import os
from helpers import BASE_ENDPOINT

def upload(session, node_id, data, file):
    """
    Uploads a file to a specific folder.

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        node_id (string):           Node id to which the file is going to be created
        data (dict):                Dict that contains file options
        file (object):              File to upload
    
    Returns:
        (list):     A list containing status code and status data

    """

    try:
        response = session.post(os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT + "/nodes/" + node_id + "/children",
                    data = data,
                    files = file
                    )
                    
        return [response.json(), response.status_code];
    except Exception as e: 
        print("File " + data["name"] + " could not be uploaded: ", e)
