from utils import find_node_info, find_site_info, add_aspects


def add_aspect_from_model(
    session, site_name, node_name, aspect_name, properties, subnode_name=""
):
    """
    Adds aspects to files and properties to improve
    the metadata associated with the file.

    Params:
        session (Session):      A session object to make requests
                                to alfresco.
        site_name (string):     The name of the site where the
                                files are stored.
        node_name (string):     The name of a node.
        aspect_name (string):   The name of the aspect to add to
                                the files.
        properties (dict):      A dict contaning the properties
                                to add to the file.
        subnode_name (string):  A subnode name (optional) where
                                the files may be.

    Returns:
        (None)
    """
    site_info = find_site_info.find_site_info(session, site_name)

    node_info = find_node_info.find_node_info(session, site_info["entry"]["id"], node_name)

    if len(subnode_name) > 0:
        subnode = find_node_info.find_node_info(session, node_info, subnode_name)

    add_aspects.add_aspects(
        session,
        subnode if subnode else node_info,
        aspect_name,
        properties,
    )
