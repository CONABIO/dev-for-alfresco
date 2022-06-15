import os

def get_zendro_deployments(zendro_session,cumulus):
    """
    Makes a query to zendro graphql endpoint to retrieve
    the deployments associated with the given cumulus.

    Params: 
        zendro_session (Session):   A session object to make 
                                    requests to zendro.
        cumulus (string):           The name of the cumulus

    Returns:
        (dict):                     A dict with the response
    """

    query = """
    {
        cumulus(search: {
            value:"%s",
            valueType: String
            field: name
            operator: eq
        }, pagination: { limit: 0 }) {
            nodesFilter(pagination: { limit: 0 }) {
                nomenclatura
                deploymentsFilter(pagination: { limit: 0 }) {
                    id
                    date_deployment
                    device {
                        serial_number
                        comments
                        device {
                            type
                        }
                    }
                }
            }
        }
    }
    """ % cumulus

    
    zendro_response = zendro_session.post(os.getenv("ZENDRO_URL")
                                + "/graphql",json={
                                    "query": query
                                })
    
    return zendro_response