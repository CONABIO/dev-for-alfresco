import os
import json
import datetime as dt
from helpers import BASE_ENDPOINT


def change_type_sonozotz(session, root_folder_id, new_type):
    """
    Change the type of a file in alfresco

    Parameters:
        session (Session):          A session object to make
                                    requests to alfresco.
        root_folder_id (string):    Id of the root folder where files
                                    are located
        new_type (string):          a string containing the name and
                                    namespace of the new type

    Returns:
        (None)
    """
    try:
        response = session.get(
            os.getenv("ALFRESCO_URL")
            + BASE_ENDPOINT
            + "/nodes/"
            + root_folder_id
            + "/children?include=properties&maxItems=2824"
        )

        data_file = open(
            "/home/jaime/Conabio/development-team-general-DGPI/jaime/alfresco_python/new_table.json"
        )

        data_json = json.load(data_file)

        updated = []
        for f in response.json()["list"]["entries"]:
            if f["entry"]["isFile"]:

                file_name = f["entry"]["name"][0 : len(f["entry"]["name"]) - 4]

                found = None
                for i in data_json:
                    if i["IdFotografia"] == file_name:
                        found = i
                        break

                prop_dict = {}
                if found:
                    for key in found:
                        prop_dict["sonozotzimage:" + key] = found[key]
                        if "fechaColecta" not in key and "fechaDeterminacion" not in key:
                            prop_dict["sonozotzimage:" + key] = found[key]
                        else:
                            prop_dict["sonozotzimage:" + key] = (
                                dt.datetime.strptime(found[key], "%d/%m/%Y").strftime(
                                    "%Y-%m-%dT%H:%M:%S.%f"
                                )[:-3]
                                + "+0000"
                            )
                else:
                    print("File " + file_name + " not found in json file")

                data = {"nodeType": new_type, "properties": prop_dict}

                update = session.put(
                    os.getenv("ALFRESCO_URL")
                    + BASE_ENDPOINT
                    + "/nodes/"
                    + f["entry"]["id"],
                    data=json.dumps(data),
                )
                if "error" in update.json().keys():
                    print(update.json())
                updated.append(update.json())

        return updated

    except Exception as e:
        print("Could not add any aspect to this file: ", e)
