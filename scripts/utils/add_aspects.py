import os
import json
from helpers import BASE_ENDPOINT


def add_aspects(session, root_folder_id, aspect, aspect_properties):
    """
    Add aspects to files in alfresco

    Parameters:
        session (Session):          A session object to make 
                                    requests to alfresco.
        root_folder_id (string):    Id of the root folder where files
                                    are located
        aspect (string):            Aspect to be added to files
        aspect_properties (dict):   Aspect properties to add to file

    Returns:
        (None) 

    """
    try:
        response = session.get(
            os.getenv("ALFRESCO_URL")
            + BASE_ENDPOINT
            + "/nodes/"
            + root_folder_id
            + "/children?include=aspectNames,properties"
        )

        for f in response.json()["list"]["entries"]:
            if f["entry"]["isFile"] and aspect not in f["entry"]["aspectNames"]:
                temp_aspect_list = f["entry"]["aspectNames"]
                temp_aspect_list.append(aspect)

                data = {
                    "aspectNames": temp_aspect_list,
                    "properties": aspect_properties
                }

                update = session.put(
                    os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT
                    + "/nodes/"
                    + f["entry"]["id"],
                    data=json.dumps(data),
                )

                print(update.json())

    except Exception as e:
        print("Could not add any aspect to this file: ", e)
