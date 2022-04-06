import os
import json
import re
import itertools
import glob
import time
import datetime as dt
from utils import login
from helpers import BASE_ENDPOINT
from helpers.globals import AUDIO_PATTERNS, VIDEO_PATTERNS, IMAGE_PATTERNS


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

    starttime = time.time()

    try:
        updated = []
        for idx, file_with_path in enumerate(files_in_dir):

            
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
                # restart time
                starttime = time.time()
                time.sleep(5)
                print("Login sucessful, continuing upload\n")

            len_of_path = len(file_with_path.split("/"))
            name_of_file = file_with_path.split("/")[len_of_path - 1]
            if re.match('[a-zA-Z_]*[0-9]*-[0-9]*-[0-9]*', name_of_file): 
                root_dir_path = file_with_path.replace(path_to_files, "").replace(
                    file_with_path.split("/")[len_of_path - 1], ""
                )

                response = session.get(
                    os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT
                    + "/nodes/"
                    + root_folder_id
                    + "/children?relativePath="+root_dir_path+"&include=aspectNames&skipCount=0&maxItems=1"
                )

                if response.status_code == 200:

                    print("Changing type of files in " + root_dir_path + "\n\n")

                    has_more_items = True
                    skip_count = 0

                    while has_more_items:

                        response = session.get(
                            os.getenv("ALFRESCO_URL")
                            + BASE_ENDPOINT
                            + "/nodes/"
                            + root_folder_id
                            + "/children?relativePath="+root_dir_path+"&include=aspectNames&skipCount=" + str(skip_count) + "&maxItems=100"
                        )

                        has_more_items = response.json()["list"]["pagination"]["hasMoreItems"]
                        data_file = open(file_with_path)

                        data_json = json.load(data_file)

                        for f in response.json()["list"]["entries"]:

                            if f["entry"]["isFile"]:

                                found = None
                                for i in data_json["MetadataFiles"].keys():
                                    len_complete_path = len(i.split("/"))
                                    filename = i.split("/")[len_complete_path - 1]
                                    if filename == f["entry"]["name"]:
                                        found = i
                                        break
                                
                                prop_dict = {}

                                if any(filetype in f["entry"]["name"] for filetype in IMAGE_PATTERNS):
                                    new_type = "sipecamImage:ImageSipecam"
                                elif any(filetype in f["entry"]["name"] for filetype in VIDEO_PATTERNS):
                                    new_type = "sipecamVideo:sipecamVideo"
                                elif any(filetype in f["entry"]["name"] for filetype in AUDIO_PATTERNS):
                                    new_type = "sipecamAudio:audiofileSipecam"
            
                                prop_dict["sipecam:NomenclatureNode"] = data_json["MetadataDevice"]["NomenclatureNode"]
                                prop_dict["sipecam:CumulusName"] = data_json["MetadataDevice"]["CumulusName"]
                                prop_dict["sipecam:EcosystemsName"] = data_json["MetadataDevice"]["EcosystemsName"]
                                prop_dict["sipecam:NodeCategoryIntegrity"] = data_json["MetadataDevice"]["NodeCategoryIntegrity"]

                                if found:
                                    file_metadata = data_json["MetadataFiles"][found]
                                    for key in file_metadata:
                                        if "date" not in key.lower():
                                            prop_dict[new_type.split(":")[0] + ":" + key] = file_metadata[key]
                                        else:
                                            try:
                                                prop_dict[new_type.split(":")[0] + ":" + key] = (
                                                    dt.datetime.strptime(file_metadata[key], "%H:%M:%S %d/%m/%Y (%Z%z)").strftime(
                                                        "%Y-%m-%dT%H:%M:%S.%f%z")
                                                )
                                            except:
                                                prop_dict[new_type.split(":")[0] + ":" + key] = (
                                                    dt.datetime.strptime(file_metadata[key], "%Y:%m:%d %H:%M:%S").strftime(
                                                        "%Y-%m-%dT%H:%M:%S.%f%z")
                                                )

                                else:
                                    print("File " + f["entry"]["name"] + " not found in json file")

                                aspects = f["entry"]["aspectNames"]

                                aspects.append("sipecam:devicemetadata")

                                data = {"aspectNames": aspects, "nodeType": new_type, "properties": prop_dict}

                                update = session.put(
                                    os.getenv("ALFRESCO_URL")
                                    + BASE_ENDPOINT
                                    + "/nodes/"
                                    + f["entry"]["id"],
                                    data=json.dumps(data),
                                )
                                if "error" in update.json().keys():
                                    print("\n\n")
                                    print(update.json())
                                    print("\n\n")
                                updated.append(update.json())

                                skip_count = skip_count + 100
                                
                                print("Updated " + f["entry"]["name"])

        return updated

    except Exception as e:
        print("Could not add any aspect to this file: ", e)
