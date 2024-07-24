import os
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

# Path to your credentials JSON file
CREDENTIALS_JSON = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_JSON = os.path.join(os.path.dirname(__file__), 'token.json')


def authenticate():
    # Load client secrets from a file
    with open(CREDENTIALS_JSON, 'r') as file:
        client_secrets = json.load(file)

    # Create the OAuth flow
    flow = InstalledAppFlow.from_client_config(
        client_secrets,
        scopes=['https://www.googleapis.com/auth/gmail.send']
    )

    # Run the local server to handle OAuth callback
    creds = flow.run_local_server(port=8080)

    # Check if credentials are valid and if email is included
    if creds and creds.token:
        token_info = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes,
            'expiry': creds.expiry.isoformat(),
            'email_address': creds.id_token.get('email', '') if creds.id_token else ''
            # Only available if using `id_token` from OAuth2
        }

        # Save token info to file
        with open(TOKEN_JSON, 'w') as token_file:
            json.dump(token_info, token_file)
        print('Token has been saved to', TOKEN_JSON)
    else:
        print("Failed to obtain valid credentials.")


if __name__ == '__main__':
    authenticate()
