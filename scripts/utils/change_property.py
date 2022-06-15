import os
import json
import time
from helpers import BASE_ENDPOINT
from utils import search


def change_property(session, aspect_or_type, property, value):
    """
    Given an aspect and a property, changes its value 
    to the filtered files in alfresco

    Parameters:
        session (Session):              A session object to make
                                        requests to alfresco.

        aspect_or_type (string):      String with the aspect to 
                                        make the files filter
        
        property (string):              The property which value
                                        we are going to change

    Returns:
        (None)

    """
    try:

        has_more_items = True

        count = 0

        files_changed = []

        while has_more_items:

            response = search(
                session,
                {
                    "query": {
                        "query":  aspect_or_type
                    },
                    "include": ["properties"],
                    "fields": ["id"],
                    "paging": {"skipCount": count, "maxItems": "100"},
                },
            )

            has_more_items = response["list"]["pagination"]["hasMoreItems"]

            for f in response["list"]["entries"]:


                data = {"properties": {
                    property: value
                }}

                update = session.put(
                    os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT
                    + "/nodes/"
                    + f["entry"]["id"],
                    data=json.dumps(data),
                )

                if update.status_code == 200:
                    files_changed.append(f["entry"]["id"])
                    print(("Changed %s with value " % property) + str(value) + " from %d files satisfactory" %  len(files_changed) )
            
            count += response["list"]["pagination"]["count"]
            print(has_more_items,response["list"]["pagination"]["count"])
        
            print(("Changed %s with value " % property) + str(value) + " from %d files satisfactory" %  len(files_changed) )

    except Exception as e:
        print("Could not remove any aspect to this file: ", e)
