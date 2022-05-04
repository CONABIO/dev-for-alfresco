import os
import json
from helpers import BASE_ENDPOINT
from utils import search


def remove_aspects(session, aspect_to_remove):
    """
    Removes given aspect from files in alfresco

    Parameters:
        session (Session):              A session object to make
                                        requests to alfresco.
        aspect_to_remove (string):      String with the aspect to remove
                                        from alfresco

    Returns:
        (None)

    """
    try:
        response = search(
            session,
            {
                "query": {
                    "query": '+ASPECT: "' + aspect_to_remove + '" AND -TYPE: "dummyType"'
                },
                "include": ["aspectNames"],
                "fields": ["id"],
                "paging": {"maxItems": "100"},
            },
        )

        has_more_items = True

        count = 0

        files_changed = []

        while has_more_items:

            has_more_items = response["list"]["pagination"]["hasMoreItems"]

            count += response["list"]["pagination"]["count"]

            for f in response["list"]["entries"]:

                current_aspects = f["entry"]["aspectNames"]


                current_aspects.remove(aspect_to_remove)

                data = {"aspectNames": current_aspects}

                files_changed.append(f["entry"]["id"])
                update = session.put(
                    os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT
                    + "/nodes/"
                    + f["entry"]["id"],
                    data=json.dumps(data),
                )

                print(update.json())
            
            response = search(
                session,
                {
                    "query": {
                        "query": '+ASPECT: "' + aspect_to_remove + '" AND -TYPE: "dummyType"'
                    },
                    "include": ["aspectNames"],
                    "fields": ["id"],
                    "paging": {"skipCount": count, "maxItems": "100"},
                },
            )
        
        print("Removed %s from %d files satisfactory" % (aspect_to_remove, len(files_changed)) )

    except Exception as e:
        print("Could not remove any aspect to this file: ", e)
