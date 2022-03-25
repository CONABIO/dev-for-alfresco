import os
from helpers import BASE_ENDPOINT

def find_site_info(session,site_name):
    """
    Makes an api request to get the id for the 
    specified name site

    Parameters:
        session (Session):      A session object to make 
                                requests to alfresco.
        site_name (string):     Name itendifier of the site

    Returns: 
        (string):               Returns the info of the site or a list
                                of entries with the same name
    """

    response = session.get(os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT + "/nodes/-root-/children?where=(nodeType=st:sites)")

    node = None

    if len(response.json()["list"]["entries"]) < 2:
        node_response = session.get(os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT + "/nodes/" + response.json()["list"]["entries"][0]["entry"]["id"] + "/children?include=aspectNames,properties")

        for entry in node_response.json()["list"]["entries"]: 
            if entry["entry"]["name"] == site_name:
                node = entry
                break

        library_response = session.get(os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT + "/nodes/" + node["entry"]["id"] + "/children?include=aspectNames,properties")

        library = None
        for entry in library_response.json()["list"]["entries"]: 
            if entry["entry"]["name"] == "documentLibrary":
                library = entry
                break
        
        return library
    
    else:
        return response.json()["list"]["entries"]
