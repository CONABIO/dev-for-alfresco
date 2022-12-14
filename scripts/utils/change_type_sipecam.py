import os
import re
import glob
import time
import json
import itertools
import traceback
import datetime as dt
from os.path import exists as file_exists

from utils import login
from utils import login_to_zendro
from helpers import BASE_ENDPOINT
from helpers.globals import AUDIO_PATTERNS, VIDEO_PATTERNS, IMAGE_PATTERNS
from helpers import get_zendro_deployments
from helpers import create_file_zendro_query


def check_log_file(files_in_dir,path_to_files):
    """
    Checks if a log file exists, if it is, then filters out
    the files that are present in the log file.

    Parameters:
        files_in_dir (list):        A list of filenames that are in a specific 
                                    location.
        path_to_files (string):     The path to the files.

    Returns:
        (list):     A list with the filtered files
    """

    dirs_with_data = []
    for file_with_path in files_in_dir:

        # taking length of the path
        len_of_path = len(file_with_path.split("/"))
        
        # obtaining the name of the file
        name_of_file = file_with_path.split("/")[len_of_path - 1]

        # extracting the full path to the file
        root_dir_path = file_with_path.replace(name_of_file, "")

        if root_dir_path not in dirs_with_data:
            dirs_with_data.append(root_dir_path)

    filename = "logs/type_n_aspects_log" + path_to_files.replace('/','-') + '.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if file_exists(filename):
        with open(filename, 'r') as f:
            lines_in_file = [line.replace('\n','') for line in f]
        
        tmp_list = [x for x in dirs_with_data if x not in lines_in_file]

        dirs_with_data = tmp_list
    
    return dirs_with_data


def search_for_json_file(files_in_dir,directory):
    """
    Searches for the json files in the different directories
    and returns the latest one given the date in the name.

    Parameters:
        files_in_dir (list):        A list of filenames that are in a specific 
                                    location.
        directory (string):         The path to the directory to search.

    Returns:
        (string):     The name and path to the json file
    """

    # filter jsons for current path
    get_json_files_for_dir = [j for j in files_in_dir if directory in j]

    # init latest date and json file url
    latest_json_file = ''
    latest_date = None
    for json_file in get_json_files_for_dir:

        # split the path taking / as delimiter
        len_of_path = len(json_file.split("/"))
        
        # obtaining the name of the file, last item in path
        name_of_file = json_file.split("/")[len_of_path - 1]

        # validate if json file matches standard name
        if re.match('[a-zA-Z_]*[0-9]*-[0-9]*-[0-9]*', name_of_file): 

            date_of_file = name_of_file.split("_")[len(name_of_file.split("_")) - 1]

            # parse it to a datetime object
            try:
                date = dt.datetime.strptime(date_of_file.replace(".json",''), '%d-%m-%Y')
            except:
                date = dt.datetime.strptime(date_of_file.replace(".json",''), '%Y-%m-%d-%H-%M-%S')

            # check if date is the latest date
            if latest_date and latest_date < date:
                latest_date = date
                latest_json_file = json_file
            elif not latest_date:
                latest_date = date
                latest_json_file = json_file
    
    return latest_json_file


def change_type_sipecam(session, root_folder_id, path_to_files, recursive):
    """
    Change the type of a file in alfresco

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        root_folder_id (string):    Id of the root folder where files
                                    are located
        path_to_files (string):     The relative path to the files
                                    location.
        recursive (boolean):        A boolean to know if the search must 
                                    be recursive in the specifed dir.

    Returns:
        (None)
    """

    if recursive:
        expression = "/**/*"
    else:
        expression = "/*"

    files_in_dir = list(
        itertools.chain.from_iterable(
            glob.iglob(path_to_files + expression + pattern, recursive=recursive)
            for pattern in [".json"]
        )
    )

    # take the start time of the script
    starttime = time.time()

    # makes a login to zendro
    zendro_session = login_to_zendro.login_to_zendro()

    # check log file to filter out files
    dirs_with_data = check_log_file(files_in_dir,path_to_files)

    try:
        updated = []
        for d in dirs_with_data:

            # filter jsons for current path
            latest_json_file = search_for_json_file(files_in_dir,d)

            # split the path taking / as delimiter
            len_of_path = len(latest_json_file.split("/"))

            # get dir path, which is the same in alfresco
            root_dir_path = latest_json_file.replace(path_to_files, "").replace(
                latest_json_file.split("/")[len_of_path - 1], ""
            )

            # make a query to relative path to check if exists
            response = session.get(
                os.getenv("ALFRESCO_URL")
                + BASE_ENDPOINT
                + "/nodes/"
                + root_folder_id
                + "/children?relativePath="+root_dir_path+"&include=aspectNames&skipCount=0&maxItems=1"
            )

            # error flag
            is_error = False

            # if request is successful then continue
            if response.status_code == 200:

                print("\n\nChanging type of files in " + root_dir_path)
                print("Total files: %d" % response.json()["list"]["pagination"]["totalItems"],"\n\n")

                has_more_items = True
                skip_count = 0

                # change type, add aspects to file for all files in location
                while has_more_items:

                    # total time since last login or script start
                    total_time = round((time.time() - starttime), 2)

                    if total_time > 2400:
                        """
                        if total time is bigger than 2400
                        or 40 minutes relogin to avoid ticket
                        expiration
                        """
                        time.sleep(5)

                        print("Re-logging in to alfresco...")

                        session = login.login()

                        time.sleep(5)
                        print("Login sucessful, loggin in to zendro now...\n")

                        zendro_session = login_to_zendro.login_to_zendro()

                        # restart time
                        time.sleep(5)
                        starttime = time.time()
                        print("Login sucessful, continuing update\n")

                    response = session.get(
                        os.getenv("ALFRESCO_URL")
                        + BASE_ENDPOINT
                        + "/nodes/"
                        + root_folder_id
                        + "/children?relativePath="+root_dir_path+"&include=aspectNames&skipCount=" + str(skip_count) + "&maxItems=100"
                    )

                    has_more_items = response.json()["list"]["pagination"]["hasMoreItems"]
                    
                    # skip to next batch
                    skip_count = skip_count + 100
                    data_file = open(latest_json_file)

                    data_json = json.load(data_file)

                    file_ids_to_upload = []
                    files_not_found = []

                    # for each file in request change type/add aspect
                    for f in response.json()["list"]["entries"]:

                        if f["entry"]["isFile"]:

                            # find match in json file with file in request
                            found = None
                            for i in data_json["MetadataFiles"].keys():
                                len_complete_path = len(i.split("/"))
                                filename = i.split("/")[len_complete_path - 1]
                                if filename.replace("AVI","mp4") == f["entry"]["name"]:
                                    found = i
                                    break
                                
                                # second check for webm
                                if filename.replace("AVI","webm") == f["entry"]["name"]:
                                    found = i
                                    break
                                        
                            prop_dict = {}

                            # select specific type for file
                            if any(filetype in f["entry"]["name"] for filetype in IMAGE_PATTERNS):
                                new_type = "sipecam:image"
                            elif any(filetype in f["entry"]["name"] for filetype in VIDEO_PATTERNS):
                                new_type = "sipecam:video"
                            elif any(filetype in f["entry"]["name"] for filetype in AUDIO_PATTERNS):
                                new_type = "sipecam:audio"
                                prop_dict["sipecam:Timeexp"] = 1.0

                            # fill data that is not included in file metadata, but corresponds to device metadata
                            prop_dict["sipecam:CumulusName"] = data_json["MetadataDevice"]["CumulusName"]
                            prop_dict["sipecam:EcosystemsName"] = data_json["MetadataDevice"]["EcosystemsName"]
                            prop_dict["sipecam:NodeCategoryIntegrity"] = data_json["MetadataDevice"]["NodeCategoryIntegrity"]
                            prop_dict["sipecam:NomenclatureNode"] = data_json["MetadataDevice"]["NomenclatureNode"]
                            prop_dict["sipecam:DateDeployment"] = data_json["MetadataDevice"]["DateDeployment"]

                            if found:
                                file_metadata = data_json["MetadataFiles"][found]
                                for key in file_metadata:
                                    if "date" not in key.lower():
                                        if "GPS" in key:
                                            prop_dict[new_type.split(":")[0] + ":" + key.replace("GPS",'')] = file_metadata[key]
                                        elif "FileSize" in key:
                                            if "GiB" in file_metadata[key]:
                                                file_size = float(file_metadata[key].replace(" GiB",'')) * 1073741824
                                            elif "MiB" in file_metadata[key]:
                                                file_size = float(file_metadata[key].replace(" MiB",'')) * 1048576
                                            elif "KiB" in file_metadata[key]:
                                                file_size = float(file_metadata[key].replace(" KiB",'')) * 1024
                                            elif "GB" in file_metadata[key]:
                                                file_size = float(file_metadata[key].replace(" MB",'')) * 1000000000
                                            elif "MB" in file_metadata[key]:
                                                file_size = float(file_metadata[key].replace(" MB",'')) * 1000000
                                            elif "kB" in file_metadata[key]:
                                                file_size = float(file_metadata[key].replace(" kB",'')) * 1000
                                            elif "B" in file_metadata[key]:
                                                file_size = int(file_metadata[key].replace(" B",''))
                                            # convert filesize to bytes
                                            prop_dict[new_type.split(":")[0] + ":" + key] = int(file_size)
                                        elif "Duration" in key:
                                            if isinstance(file_metadata[key],str):
                                                if ":" in file_metadata[key]:
                                                    duration = (int(file_metadata[key].split(":")[0])*60)*60 + int(file_metadata[key].split(":")[1])*60 + int(file_metadata[key].split(":")[2])
                                                elif "s" in file_metadata[key]:
                                                    duration = float(file_metadata[key].replace(" s",''))
                                            else:
                                                duration = file_metadata[key]
                                            prop_dict[new_type.split(":")[0] + ":" + key] = duration
                                        else:
                                            prop_dict[new_type.split(":")[0] + ":" + key] = file_metadata[key]
                                    else:
                                        if "datetime" in key.lower() and "original" not in key.lower():
                                            if "DateTime" != key:
                                                key_name = new_type.split(":")[0] + ":DateTimeOriginal" 
                                            else:
                                                key_name = new_type.split(":")[0] + ":" + key + "Original"
                                        else:
                                            key_name = new_type.split(":")[0] + ":" + key
                                        try:
                                            prop_dict[key_name] = (
                                                dt.datetime.strptime(file_metadata[key], "%H:%M:%S %d/%m/%Y (%Z%z)").strftime(
                                                    "%Y-%m-%dT%H:%M:%S.%f%z")
                                            )
                                        except:
                                            prop_dict[key_name] = (
                                                dt.datetime.strptime(file_metadata[key], "%Y:%m:%d %H:%M:%S").strftime(
                                                    "%Y-%m-%dT%H:%M:%S.%f%z")
                                            )

                            else:
                                print("File " + f["entry"]["name"] + " not found in json file")
                                files_not_found.append(f["entry"]["name"])

                            aspects = f["entry"]["aspectNames"]

                            # add aspects for common properties
                            aspects.append("sipecam:common")
                            aspects.append("sipecam:fileDetails")

                            # aspects for common properties in specific types
                            if any(filetype in f["entry"]["name"] for filetype in IMAGE_PATTERNS):
                                aspects.append("sipecam:imageVideoCommons")
                            elif any(filetype in f["entry"]["name"] for filetype in VIDEO_PATTERNS):
                                aspects.append("sipecam:imageVideoCommons")
                                aspects.append("sipecam:audioVideoCommons")
                            elif any(filetype in f["entry"]["name"] for filetype in AUDIO_PATTERNS):
                                aspects.append("sipecam:audioVideoCommons")

                            # collect update data
                            data = {"aspectNames": aspects, "nodeType": new_type, "properties": prop_dict}

                            # update properties request
                            update = session.put(
                                os.getenv("ALFRESCO_URL")
                                + BASE_ENDPOINT
                                + "/nodes/"
                                + f["entry"]["id"],
                                data=json.dumps(data),
                            )

                            # if theres an error, output to console
                            if "error" in update.json().keys():
                                is_error = True
                                print("\n\n")
                                print(update.json())
                                print("\n\n")
                            updated.append(update.json())

                            print("Updated " + f["entry"]["name"])

                            if found:
                                prop_dict.update({"id": f["entry"]["id"], "mimeType": f["entry"]["content"]["mimeType"], "fullPath": found})
                                file_ids_to_upload.append(prop_dict)
                    
                    if len(files_not_found) > 0:
                        filename = "logs/files_n_dirs_w_no_metadata" + dt.datetime.now().strftime("%Y-%m-%d") + '.txt'
                        with open(filename, 'a') as log_file:
                            log_file.writelines("%s: [\n" % d)
                        
                            for i in files_not_found:
                                    log_file.writelines("\t%s\n" % i)
                            
                            log_file.writelines("]\n")
                        


                    print("\nUploading data to zendro...")
                    time.sleep(5)
                    zendro_response = get_zendro_deployments.get_zendro_deployments(zendro_session,data_json["MetadataDevice"]["CumulusName"])
                    
                    query = create_file_zendro_query.create_file_zendro_query(file_ids_to_upload,zendro_response)

                    time.sleep(5)
                    response = zendro_session.post(os.getenv("ZENDRO_URL")
                            + "/graphql",json={
                                "query": "mutation {" +
                                    query + "}"
                            })
                    
                    time.sleep(5)
                    print("\nDone! continuing with alfresco...\n")
                    
                    file_ids_to_upload = []

            if not is_error:
                filename = "logs/type_n_aspects_log" + path_to_files.replace('/','-') + '.txt'
                with open(filename, 'a') as log_file:
                    log_file.writelines("%s\n" % d)

        return updated

    except Exception as e:
        print(traceback.format_exc())
        print("Could not add any aspect to this file: ", e)
