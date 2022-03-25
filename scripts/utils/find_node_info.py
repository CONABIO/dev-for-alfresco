import os
from helpers import BASE_ENDPOINT


def find_node_info(session, site_id, node_name):
    """
    Makes an api request to get the id for the
    specified node (folder)

    Parameters:
        session (Session):  A session object to make
                            requests to alfresco.
        site_id (string):   Name itendifier of the site
        node_name (string): Name identifier of the node folder

    Returns:
        (string):           Returns the id of the node
    """

    response = session.get(
        os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/nodes/" + site_id + "/children"
    )

    node = None

    for entry in response.json()["list"]["entries"]:
        if entry["entry"]["name"] == node_name:
            node = entry
            break

    if node:
        return node["entry"]["id"]
    else:
        return node
