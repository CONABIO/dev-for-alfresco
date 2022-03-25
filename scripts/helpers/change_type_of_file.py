from utils.find_site_info import find_site_info
from utils.change_type_sipecam import change_type_sipecam


def change_type_of_file(session, site_name, path_to_files):
    """
    Change the type to files and adds properties to improve
    the metadata associated with the file.

    Params:
        session (Session):      A session object to make requests
                                to alfresco.
        site_name (string):     The name of the site where the
                                files are stored.
        path_to_files (string): The relative path to the files
                                location.

    Returns:
        (string):   Info string with the amount of updated files.
    """
    site_info = find_site_info(session, site_name)

    updated = change_type_sipecam(session, site_info["entry"]["id"], path_to_files, True)

    return updated
