
from datetime import datetime, timedelta


def nearest(items, pivot):
    return min(items, key=lambda x: abs(datetime.strptime(x["date_deployment"], '%Y-%m-%dT%H:%M:%S.%fZ') - pivot))

def create_file_zendro_query(files_with_props,zendro_response):
    """
    Creates a graphql query to upload files info from alfresco to
    zendro.

    Parameters:
        files_with_props (list):  A list with files ids and info to upload to zendro.
        zendro_response (dict):   A dict containing the info of deployments.

    Returns:
        (string):       A string with the query to create entries in zendro.
    """

    query = ""

    types_dict = {
        "image": "camara",
        "video": "camara",
        "audio": "grabadora"
    }
    for idx,i in enumerate(files_with_props):
        date_file = i["sipecam:DateDeployment"]
        node = i["sipecam:NomenclatureNode"]

        close_deployment = None
        if "sipecam:SerialNumber" in i:
            device_serial = i["sipecam:SerialNumber"]
            temp =  [d for d in zendro_response.json()["data"]["cumulus"][0]["nodesFilter"] if d["nomenclatura"] == node]

            node_deployments = []
            for el in temp:
                if types_dict[i["mimeType"].split("/")[0]] == "grabadora":
                    node_deployments = [ *node_deployments, *[d for d in el["deploymentsFilter"] if d["device"]["comments"].replace("ADM",'') == device_serial] ]
                else:
                    node_deployments = [ *node_deployments, *[d for d in el["deploymentsFilter"] if d["device"]["serial_number"] == device_serial] ]
            
            # find nearest date to date_file
            alfresco_file = datetime.strptime(date_file, '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
            close_deployment = nearest(node_deployments,alfresco_file)
        else:
            node_deployments =  [d for d in zendro_response.json()["data"]["cumulus"][0]["nodesFilter"] if d["nomenclatura"] == node]

            # find nearest date to date_file
            alfresco_file = datetime.strptime(date_file, '%Y-%m-%dT%H:%M:%S.%f%z').replace(tzinfo=None)
            deployments = [d for d in node_deployments[0]["deploymentsFilter"] if d["device"]["device"]["type"] == types_dict[i["mimeType"].split("/")[0]]]
            close_deployment = nearest(deployments,alfresco_file)
        query = query + ("d" + str(idx) + ": addFile("
             + "id_alfresco: \"" + i["id"] + "\","
             + "type: \"" + i["mimeType"] + "\","
             + "storage: \"s3\","
             + "addAssociated_deployment: " + close_deployment["id"] + ")"
             + "{ id }   "
            )

    return query