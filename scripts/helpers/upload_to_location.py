from utils import find_node_info, find_site_info, upload_files


def upload_to_location(session, site_name, path_to_files, recursive, node_name=""):
    """
    Uploads a bunch of files to a specific
    location in alfresco.

    Params:
        session (Session):      A session object to make requests
                                to alfresco.
        site_name (string):     The name of the site where the
                                files are going to be uploaded
        path_to_files (string): The path to a location where the
                                files are stored
        recursive (boolean):    A boolean to know if upload  must be recursive
                                in the specifed dir, and should preserve the
                                structure of dirs inside.
        node_name (string):     The name of a node inside the
                                site, to store the files in a
                                more ordered structure (optional)

    Returns:
        (string):       A string indicating the number of files that
                        where uploaded.
    """

    site_info = find_site_info.find_site_info(session, site_name)

    node_info = None
    if len(node_name) > 0:
        node_info = find_node_info.find_node_info(
            session, site_info["entry"]["id"], node_name
        )

    uplodaded_files = upload_files.upload_files(
        session,
        node_info if node_info else site_info["entry"]["id"],
        path_to_files,
        recursive,
    )

    if len(uplodaded_files) > 0:
        return "Uploaded %d files to alfresco" % len(uplodaded_files)
