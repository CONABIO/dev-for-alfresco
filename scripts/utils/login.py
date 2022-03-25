import os
import json
import base64
import requests
from helpers import AUTH_ENDPOINT

def login():
    """
    Tries a login to alfresco api and returns a session
    object with credentials 
    Returns: 
        session (Session):  A session object to make 
                            requests to zendro.
    """
    try:
        auth = {
            "userId": os.getenv("ALFRESCO_USER"),
            "password": os.getenv("ALFRESCO_PASSWORD"),
        }

        login = requests.post(os.getenv("ALFRESCO_URL") + AUTH_ENDPOINT + "/tickets",data=json.dumps(auth))

        base64_login = base64.b64encode(bytes(login.json()["entry"]["id"], 'utf-8')).decode()

        # se crea un objeto de Session para hacer requests
        session = requests.Session()
        # se establece bearer token
        session.headers.update({'Authorization': 'Basic ' + base64_login})

        return session
    except Exception as e:
        print("Login failed: ",e)
