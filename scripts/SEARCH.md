# Using REST API to search in Alfresco

There are several ways to make a search in alfresco, wheter using the search query, solr, or by the api base endpoint to find sites, folders and files by a term.

In these scripts the search query is used. This search query is condensed in a python function which has the following structure:

    search(
        session,
        query
    )

where the params are:

    session (Session):  A session object to make
                        requests to alfresco.
    query (dict):       A dict containing the seach
                        query.

and the response:

    (dict):         A dict containing the response
                    of the search query

The search query can be in three diferent languages, which are cmis, lucene, and the default search language, the Alfresco Full Text Search (afts). A simple example of the default search language is the following

    {
        "query": {
            "query": '+TYPE:"sonozotz:audio" AND (sonozotz:altitud:"117")',
            "language": "afts",
        },
        "include": ["properties"],
        "sort": [{"type": "FIELD", "field": "cm:name", "ascending": "false"}],
    }
    
in this example the most important parameter is the "query", while the other ones are optional. In the query parameter we can find a "query" and the "language", in here the "language" param is redundant, because "afts" is the default language, so if the query is written using this language, this param can be omitted. In this query, we are searching the files that share the type "sonozotz:audio" and also has the property "sonozotz:altitud:'117'".

We can also request to include certain fields in our query, to do that we use "include" and a list of the fields we wish to retreive from our request. In the example above we include "properties", so this brings us all the properties with the filtered files.

We can sort the results of the query with "sort", and we can include many sorts in our search, so we can sort by the name and the type, or a certain aspect, etc.

The result of our example returns the next json:

    {
    "list": {
        "pagination": {
            "count": 3,
            "hasMoreItems": false,
            "totalItems": 3,
            "skipCount": 0,
            "maxItems": 100
        },
        "context": {
            "consistency": {
                "lastTxId": 107684
            }
        },
        "entries": [
            {
                "entry": {
                    "isFile": true,
                    "createdByUser": {
                        "id": "admin",
                        "displayName": "Administrator"
                    },
                    "modifiedAt": "2022-02-24T19:12:48.647+0000",
                    "nodeType": "sonozotz:audio",
                    "content": {
                        "mimeType": "audio/x-wav",
                        "mimeTypeName": "WAV Audio",
                        "sizeInBytes": 2482920,
                        "encoding": "UTF-8"
                    },
                    "parentId": "baba3422-05c5-4d3a-a9a2-599c1aaf7040",
                    "createdAt": "2022-02-24T18:55:26.533+0000",
                    "isFolder": false,
                    "search": {
                        "score": 8.428757
                    },
                    "modifiedByUser": {
                        "id": "admin",
                        "displayName": "Administrator"
                    },
                    "name": "010801-0036-E01.wav",
                    "location": "nodes",
                    "id": "a11f70b2-6c5e-4702-b64e-b629bba8c526",
                    "properties": {
                        "sonozotz:tipoHabitat": "Arroyo con remanentes de vegetacion riparia y predominancia de chaparral",
                        "sonozotz:IdFotografia": "010801-0036-01-AAGC",
                        "sonozotz:ambienteGrabacion": "Borde de vegetacion sobre agua",
                        ...
                    }
                }
            },
            ...

if we only search for the type "sonozotz:audio" we obtain the following result

    {
        "list": {
            "pagination": {
                "count": 100,
                "hasMoreItems": true,
                "totalItems": 101,
                "skipCount": 0,
                "maxItems": 100
            },
            "entries": [
            ...
            ]
        }
    }

currently there are 2032 files with the type "sonozotz:audio" in our alfresco installation, but alfresco says that the totalItems are 101. These could be related to how the search service works, but a workaround this issue is to include a dummy type in the filter of our search query like the example below

    {
      "query": {
        "query": "+TYPE:\"sonozotz:audio\" AND -TYPE:\"dummyType\""
      }
    }

and this returns

    {
        "list": {
            "pagination": {
                "count": 100,
                "hasMoreItems": true,
                "totalItems": 2032,
                "skipCount": 0,
                "maxItems": 100
            },
            ...
        }
    }

which includes the totalItems with the correct number of items with the type "sonozotz:audio". 