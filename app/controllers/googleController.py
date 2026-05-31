# DESATIVADO — integração Google não utilizada no momento.
# O código abaixo é preservado para referência mas não está em uso.
# Para reativar: descomentar o bloco, instalar as deps Google e configurar credentials.json.

# import os.path
# from flask import jsonify, redirect, render_template, request, url_for
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request as GoogleRequest
#
# SCOPES = [
#     'https://www.googleapis.com/auth/drive.file',
#     'https://www.googleapis.com/auth/spreadsheets',
# ]
#
# TOKEN_DIR = '/app/data'
# TOKEN_PATH = os.path.join(TOKEN_DIR, 'token.json')
# REDIRECT_URI = 'http://localhost:8000/auth/oauth2callback'
#
# def criar_fluxo():
#     return Flow.from_client_secrets_file(
#         'credentials.json',
#         scopes=SCOPES,
#         redirect_uri=REDIRECT_URI
#     )
#
# def NovaCredenciaisGoogle():
#     flow = criar_fluxo()
#     auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
#     return render_template("pages/Google/configGoogle.html", auth_url=auth_url)
#
# def oauth2callback():
#     current_url = request.url
#     if "localhost" in current_url:
#         current_url = current_url.replace("https://", "http://")
#     try:
#         flow = criar_fluxo()
#         flow.fetch_token(authorization_response=request.url)
#         creds = flow.credentials
#         if not os.path.exists(TOKEN_DIR):
#             os.makedirs(TOKEN_DIR)
#         with open(TOKEN_PATH, 'w') as token_file:
#             token_file.write(creds.to_json())
#         return redirect(url_for("trainings.list"))
#     except Exception as e:
#         return jsonify({"status": "erro", "mensagem": f"Erro na validação do token: {str(e)}"}), 400
#
# def obter_credenciais():
#     creds = None
#     if os.path.exists(TOKEN_PATH):
#         creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
#     if creds and creds.expired and creds.refresh_token:
#         try:
#             creds.refresh(GoogleRequest())
#             with open(TOKEN_PATH, 'w') as token_file:
#                 token_file.write(creds.to_json())
#         except Exception as e:
#             print(f"Erro ao renovar o token: {e}")
#             return None
#     if creds and creds.valid:
#         return creds
#     return None
#
# def InicializarServicosGoogle():
#     creds = obter_credenciais()
#     if not creds:
#         raise Exception("Autenticação do Google ausente ou expirada. Reconecte sua conta.")
#     forms_service = build('forms', 'v1', credentials=creds)
#     drive_service = build('drive', 'v3', credentials=creds)
#     return forms_service, drive_service