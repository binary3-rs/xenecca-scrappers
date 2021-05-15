from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def refresh_token_if_expired(credentials):
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())


def obtain_credentials(credentials_file, scopes):
    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
    return flow.run_local_server(port=1337)
