import os
import json
from helpers import BASE_ENDPOINT


def create_sites(session, site_name, site_description, site_visibility):
    """
    Creates a site in alfresco

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        site_name (string):         The name of the site to be created
        site_description (string):  A string conatining a short description of the site.
        site_visibility (string):   A string defining the visibility of the site.

    Returns:
        (string):           Returns the info of recent created site.
    """

    response = session.post(
        os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/sites",
        data = json.dumps({
            "title": site_name,
            "description": site_description,
            "visibility": site_visibility
        })
    )

    return response.json()
