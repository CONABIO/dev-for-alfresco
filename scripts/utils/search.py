import os
import json


def search(session, query):
    """
    Makes a post with search query
    to alfresco

    Parameters:
        session (Session):  A session object to make
                            requests to alfresco.
        query (dict):       A dict containing the seach
                            query.

        Returns:
            (dict):         A dict containing the response
                            of the search query
    """

    try:
        response = session.post(
            os.getenv("ALFRESCO_URL")
            + "/alfresco/api/-default-/public/search/versions/1/search",
            data=json.dumps(query),
        )

        return response.json()
    except Exception as e:
        print("Bad search query: ", e)
