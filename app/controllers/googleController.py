import os.path
from flask import jsonify,redirect, render_template, request,url_for
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request as GoogleRequest

# Escopos para gerenciar o corpo do formulário e visualizar os arquivos no Drive
SCOPES = [
    # Permite criar pastas, mover arquivos e ler/escrever dados nos arquivos criados pelo seu app (Recomendado)
    'https://www.googleapis.com/auth/drive.file',
    
    # Permite criar e ler/escrever dados em qualquer Planilha Google da conta
    'https://www.googleapis.com/auth/spreadsheets',
]

# Configuração de caminhos persistentes no Docker
TOKEN_DIR = '/app/data'
TOKEN_PATH = os.path.join(TOKEN_DIR, 'token.json')

# URL exata que o blueprint monta: /auth + /oauth2callback
REDIRECT_URI = 'http://localhost:8000/auth/oauth2callback'

def criar_fluxo():
    """Gera o objeto de fluxo OAuth2 apontando para o arquivo de credenciais."""
    return Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def NovaCredenciaisGoogle():
    """Gera a URL de autenticação e renderiza a página de configuração."""
    flow = criar_fluxo()
    # Gera a URL externa de consentimento do Google
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
    return render_template("pages/Google/configGoogle.html", auth_url=auth_url)

@staticmethod
def oauth2callback():
    """Recebe o código enviado pelo Google, valida e salva o token no Docker."""
    current_url = request.url
    
    if "localhost" in current_url:
        current_url = current_url.replace("https://", "http://")

    try:
        flow = criar_fluxo()
        flow.fetch_token(authorization_response=request.url)
    
        creds = flow.credentials
        
        # Garante que o diretório persistente no Docker existe antes de gravar
        if not os.path.exists(TOKEN_DIR):
            os.makedirs(TOKEN_DIR)
            
        # Salva as credenciais permanentemente no volume
        with open(TOKEN_PATH, 'w') as token_file:
            token_file.write(creds.to_json())
            
        return redirect(url_for("trainings.list"))
        
    except Exception as e:
        return jsonify({
            "status": "erro", 
            "mensagem": f"Erro na validação do token: {str(e)}",
            "dica": "Verifique se a variável SCOPES no seu código Python está IDÊNTICA aos escopos ativados na tela de consentimento do Google Cloud."
        }), 400

def obter_credenciais():
    """Resgata, valida e renova as credenciais do Google salvas no Docker."""
    creds = None

    # 1. Verifica se o arquivo de token já existe no volume do Docker
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # 2. Se o token expirou mas temos o refresh_token, renova em background
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(GoogleRequest())
            # Atualiza o arquivo token.json com a nova data de expiração
            with open(TOKEN_PATH, 'w') as token_file:
                token_file.write(creds.to_json())
        except Exception as e:
            print(f"Erro ao renovar o token: {e}")
            return None

    # 3. Se as credenciais forem válidas, retorna o objeto creds
    if creds and creds.valid:
        return creds

    return None

def InicializarServicosGoogle():
    """Instancia os serviços do Google (Forms e Drive) para uso em outras partes do app."""
    creds = obter_credenciais()
    
    if not creds:
        raise Exception("Autenticação do Google ausente ou expirada. Reconecte sua conta.")

    # Cria e retorna os serviços prontos para uso
    forms_service = build('forms', 'v1', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)
    
    return forms_service, drive_service
