from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

def indexar_url(url_para_indexar):
    # Escopo da API de Indexação
    SCOPES = ['https://www.googleapis.com/auth/indexing']
    # Nome do seu arquivo de credenciais que você deverá baixar
    KEY_FILE = 'service_account.json' 

    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE, SCOPES)
    service = build('indexing', 'v3', credentials=credentials)

    batch = {
        'url': url_para_indexar,
        'type': 'URL_UPDATED'
    }

    response = service.urlNotifications().publish(body=batch).execute()
    return response