from googleapiclient.discovery import build
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Escopos para gerenciar o corpo do formulário e visualizar os arquivos no Drive
SCOPES = [
'.../auth/drive.file',
'.../auth/docs',
'.../auth/drive.photos.readonly',
'.../auth/forms.body',
'.../auth/forms.body.readonly',
'.../auth/forms.responses.readonly',
'.../auth/spreadsheets',
'.../auth/spreadsheets.readonly',
'.../auth/drive',
'.../auth/drive.readonly'
]
TOKEN_PATH = 'data/token.json'

def CredenciaisGoogle():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(host='0.0.0.0', port=8080, prompt='consent', open_browser=False)
            
        # Cria a pasta 'data' se ela não existir no container
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
            
    # Inicializa os serviços das APIs
    forms_service = build('forms', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    return forms_service, drive_service, sheets_service