from dotenv import load_dotenv
import os
import json
from utils import create_sites, search, login, remove_aspects
from helpers import *

# load dotenv vars located in .env file
load_dotenv()

session = login()

"""

    HOWTO: scripts for better handling alfresco's api

    This scripts are a compendium of alfresco api endpoints
    enclosed in several functions to make the requests for
    creating, listing, update and manage the nodes, sites, and
    also aspects and types of files in an alfresco instalation.

    Next up is the list of the current available functions for 
    certain actions in alfresco with a short description for each one:

    * Create sites:

        This function creates a site in alfresco, receives a 
        session object, the name of the site, a title in a human
        readable form, and the visibility, e.g.:

        create_sites(session, "cumulo-92", "Cumulo 92", "PUBLIC")

    *  Create folders inside a site:

        This function creates a folder inside a site, and also can
        create subfolders inside in this folder. Receives as parameters
        a session object, the name of the site, the name of the folder,
        the title of the folder in a human readable form, and the list
        of subfolders with name and title (in that order), e.g.:

        create_folder_in_site(
            session, 
            "cumulo-92",
            "1338",
            "Nodo 1338",
            [
                ["photos", "Photos"],
                ["videos", "Videos"]
            ]
        )

    * Upload files to alfresco

        This function uploads several files located inside a dir to a 
        specific location in alfresco. Receives a session object, the 
        site name, the path to the dir where the files are located, and
        optionally, the name of a node inside the site, if the files are
        required to be stored in a certain location in the site. Also this
        function classifies the files by audio, video and photo, filtering
        the files inside the dir, and created inside the location in alfresco
        three folders with the name: "Audios", "Fotos" and "Videos".

        upload_to_location(
            session, 
            "cumulo-92", 
            /home/<user>/<path>/<to>/<dir>,
            True
            "1338"
        )

    * Add aspects to files

        Add aspects to files, so it can be possible to add some custom
        properties (like metadata) to a file. Receives a session object,
        the site name where the files are located, also the node name, and
        optionally a subnode name. It also receives the aspect name in the
        way that is declared in alfresco, and the properties that are going
        to be associated to the file, e.g.:

        add_aspect_from_model(
            session, 
            "cumulo-92",
            "1338",
            "sonozotz:audio", 
            { "sonozotz:title": "prueba" }, 
            "fotos"
        )

    * Change type of files

        Similar to the aspects, one can change the type of a file to include in
        its metadata more properties. The difference from adding aspects to 
        change the type of a file is that one can remove an aspect when isn't
        needed anymore, but change the type back to the default one is hard or
        it can't be done. This function receives a session object, the site name
        where the files are, the node name, and the new type.

        change_type_of_file(
            session,
            "cumulo-92",
            "1338",
            "sonozotzimage:voucher"
        )

    * Search

        A function to make a search query in alfresco. This function makes a post
        to the search endpoint with some data in json format wich includes the
        search query. The search query can be in cmis, lucene, and the default 
        search language, the Alfresco Full Text Search (afts). The function only
        receives the session object and the dict with the query, e.g.:

        search(
            session,
            {
                "query": {
                    "query": '+TYPE:"sonozotz:audio" AND (sonozotz:altitud:"117")',
                    "language": "afts",
                },
                "include": ["properties"],
                "sort": [{"type": "FIELD", "field": "cm:name", "ascending": "false"}],
            },
        )

        In the example afts language is specifed, but it is not required as is the 
        default language.

        Other helpful properties for the query are:

            "paging": {
                "maxItems": "25",
                "skipCount": "10"
            }
            
            "include": [
                "aspectNames"
            ]

        More info about the search query can be found here: 
        https://docs.alfresco.com/content-services/latest/develop/rest-api-guide/searching/#searchbyquery

"""

if "Authorization" in session.headers.keys():
    """
    If auth is present in session headers, then
    the login was succesful. So you can try any
    of the function above inside this if.
    """
    # res = search(
    #     session,
    #     {
    #         "query": {
    #             "query": '+TYPE:"sipecamImage:ImageSipecam" AND (sipecam:CumulusName:"92")',
    #             "language": "afts",
    #         },
    #         "paging": {
    #             "maxItems": "10",
    #         },
    #     },
    # )

    # ids = []
    # for i in res["list"]["entries"]:
    #     ids.append(i["entry"]["id"])

    # d = session.post(
    #     os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/downloads/",
    #     data=json.dumps({"nodeIds": ids}),
    # )

    # download_id = d.json()["entry"]["id"]

    # d_status = session.get(
    #     os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/downloads/" + download_id
    # )

    # download_status = d_status.json()["entry"]["status"]

    # while download_status != "DONE":
    #     d_status = session.get(
    #         os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/downloads/" + download_id
    #     )
        
    #     download_status = d_status.json()["entry"]["status"]
    
    # zip_file = session.get(
    #         os.getenv("ALFRESCO_URL") + BASE_ENDPOINT + "/nodes/" + download_id + "/content"
    #     )

    # with open("data.zip",'wb') as output_file:
    #     output_file.write(zip_file.content)
    # print('Downloading Completed')

    # remove_aspects(session,"sipecam:fileDetails")

    res = change_type_of_file(session,"sipecam","")

    print("updated %d files" % len(res))

    # print(ids)