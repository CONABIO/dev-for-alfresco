import os
import json
from helpers import BASE_ENDPOINT


def create_folder(session, node_id, folder_name, folder_title,folder_fescription):
    """
    Creates a folder in a specific node

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        node_id (string):           Node id to which the folder is going to be created
        folder_name (string):       The name of the folder to be created
        folder_title (string):      The title of the folder in human readable form
        folder_fescription (string): A string containing a short description for the folder

    Returns:
        (string):           Returns the info of recent created folder.
    """

    response = session.post(
        os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/nodes/"+ node_id + "/children",
        data = json.dumps({
            "name": folder_name,
            "nodeType": "cm:folder",
            "properties": {
                "cm:title": folder_title,
                "cm:description": folder_fescription
            },
        })
    )

    return response.json()
