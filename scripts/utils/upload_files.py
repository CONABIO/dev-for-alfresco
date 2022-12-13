import time
import os
from os.path import exists as file_exists
import itertools
from datetime import datetime
import glob
from helpers.globals import FILE_PATTERNS
from utils.upload import upload
from utils import login


def upload_files(session, node_id, dir_path, recursive, file_identifier=""):
    """
    Uploads the files stored in a specific dir
    to alfresco

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        node_id (string):           Node id to which the file is going to be created
        dir_path (string):          The name and path of the dir where files are stored
        recursive (boolean):        A boolean to know if upload  must be recursive
                                    in the specifed dir, and should preserve the
                                    structure of dirs inside.
        file_identifier (string):   File identifier for all files inside a dir

    Returns:
        (string):           Returns the info of recent created site.
    """
    
    starttime = time.time()

    if recursive:
        expression = "/**/*"
    else:
        expression = "/*"

    files_in_dir = list(
        itertools.chain.from_iterable(
            glob.iglob(dir_path + expression + pattern, recursive=recursive)
            for pattern in FILE_PATTERNS
        )
    )

    recent_uploaded = "recent_uploaded/uploaded-" + datetime.now().strftime("%Y-%m-%d-%H-%M-%s") + ".txt"
    os.makedirs(os.path.dirname(recent_uploaded), exist_ok=True)

    filename = "logs/upload_log" + dir_path.replace('/','-') + '.txt'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if file_exists(filename):
        with open(filename, 'r') as f:
            lines_in_file = [line.replace('\n','') for line in f]
        
        tmp_list = [x for x in files_in_dir if x not in lines_in_file]

        files_in_dir = tmp_list

    total_files = len(files_in_dir)

    try:
        files_uploaded = []
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
            root_dir_path = file_with_path.replace(dir_path, "").replace(
                file_with_path.split("/")[len_of_path - 1], ""
            )

            filetype = [filetype for filetype in FILE_PATTERNS if filetype in name_of_file]

            data = {
                "name": (
                    name_of_file.replace(filetype[0],'')
                    + file_identifier
                    + filetype[0]
                ),
                "nodeType": "cm:content",
            }

            data["relativePath"] = root_dir_path

            data["properties"] = {
                "cm:title": (
                    name_of_file.replace(filetype[0],'')
                    + file_identifier
                    + filetype[0]
                )
            }

            print("Uploading " + data["name"] + " file...")

            files = {"filedata": open(file_with_path, "rb")}
            upload_response = upload(session, node_id, data, files)
            if upload_response[1] and upload_response[1] == 201:
                files_uploaded.append(upload_response[0])

                # print log file of files in this upload
                with open(recent_uploaded, 'a') as log_file:
                    log_file.writelines("%s\n" % file_with_path)
                    
                print("Uploaded " + data["name"])

                filename = "logs/upload_log" + dir_path.replace('/','-') + '.txt'
                with open(filename, 'a') as log_file:
                    log_file.writelines("%s\n" % file_with_path)

            elif upload_response[1] and upload_response[1] == 409:
                if "already exists" in upload_response[0]["error"]["errorKey"]:
                    print("File " + data["name"] + " already uploaded")

            else:
                print("An error ocurred, file " + data["name"] + " cannot be uploaded")
                print(upload_response)

            print("Uploaded file " + str(idx + 1) + " of " + str(total_files))
            print("\n\n")

        return files_uploaded
    except Exception as e:
        print("An error ocurred in file upload: ", e)
