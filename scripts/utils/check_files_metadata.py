import os
import re
import glob
import time
import json
import itertools
import traceback
import datetime as dt
from os.path import exists as file_exists

from helpers import BASE_ENDPOINT
from helpers.globals import FILE_PATTERNS


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
            date = dt.datetime.strptime(date_of_file.replace(".json",''), '%d-%m-%Y')

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

    # check log file to filter out files
    dirs_with_data = check_log_file(files_in_dir,path_to_files)

    try:
        bad_files = []
        for d in dirs_with_data:

            # filter jsons for current path
            latest_json_file = search_for_json_file(files_in_dir,d)

            # split the path taking / as delimiter
            len_of_path = len(latest_json_file.split("/"))

            # get dir path, which is the same in alfresco
            root_dir_path = latest_json_file.replace(
                latest_json_file.split("/")[len_of_path - 1], ""
            )

            files_in_dir = list(
                itertools.chain.from_iterable(
                    glob.iglob(root_dir_path + expression + pattern, recursive=recursive)
                    for pattern in FILE_PATTERNS
                )
            )

            for f in files_in_dir:

                data_file = open(latest_json_file)
                data_json = json.load(data_file)

                # find match in json file with file in request
                found = None
                for i in data_json["MetadataFiles"].keys():
                    len_complete_path = len(i.split("/"))
                    filename = i.split("/")[len_complete_path - 1]
                    if filename.replace("AVI","mp4") == f["entry"]["name"]:
                        found = i
                        break

                if not found:
                    bad_files.append(f)
                
                

        return bad_files

    except Exception as e:
        print(traceback.format_exc())
        print("Could not add any aspect to this file: ", e)
