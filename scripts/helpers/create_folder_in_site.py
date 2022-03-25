from utils import create_folder, find_site_info


def create_folder_in_site(session, site_name, node_name, node_title, subnodes):
    """
    Creates a folder inside a site, and also subfolders
    to improve the structure of files.

    Params:
        session (Session):      A session object to make requests
                                to alfresco.
        site_name (string):     The name of the site where the
                                folder is going to be created.
        node_name (string):     The name of a node that is going
                                to be created inside the site.
        node_title (string):    A human readable title for the
                                folder.
        subnodes (list):        A list of subfolders to create
                                inside the parent folder. The list
                                should include name and title, in
                                that order (optional)
                                e.g: [ ["photos","Photos folder"], ... ]

    Returns:
        (string):       A string indicating the  recent created
                        folder and its id.
    """

    site_info = find_site_info.find_site_info(session, site_name)

    response = create_folder.create_folder(
        session, site_info["entry"]["id"], node_name, node_title, ""
    )

    if "entry" in response and "id" in response["entry"] and len(subnodes) > 0:
        for subnode in subnodes:
            create_folder(session, response["entry"]["id"], subnode[0], subnode[1], "")

        return (
            "Created folder for node "
            + response["entry"]["name"]
            + " with id "
            + response["entry"]["id"]
        )
