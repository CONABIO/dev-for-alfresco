# Scripts Alfresco

Este conjunto de scripts recopila varias consultas útiles que se pueden hacer al API REST de Alfresco. Para iniciar este script es necesario tener intalado python 3.8 o superior, y los requirements que se encuentran en requirements.txt

## Primeros pasos

Instalar los requirements con el siguiente comando:

    pip install -r requirements.txt

También es necesario establecer algunas variables de ambiente en un archivo .env, en el root del proyecto:

    # Alfresco credentials
    ALFRESCO_URL="[alfresco url]"
    ALFRESCO_USER=alfresco_user  
    ALFRESCO_PASSWORD=alfresco_password

una vez listo esto el script se puede correr como cualquier script de python: `python main.py` 