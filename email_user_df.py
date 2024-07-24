import yagmail
from google.oauth2.credentials import Credentials
import pandas as pd
import os

CREDENTIALS_JSON = os.path.join(os.path.dirname(__file__), 'credentials.json')
TOKEN_JSON = os.path.join(os.path.dirname(__file__), 'token.json')


def authenticate_gmail():
    """
    Authenticates the user using OAuth 2.0 and returns an authenticated yagmail SMTP client.
    """
    # Check if token file exists
    if os.path.exists(TOKEN_JSON):
        creds = Credentials.from_authorized_user_file(TOKEN_JSON)
    else:
        raise FileNotFoundError("Token file not found. Please run the OAuth flow to obtain the token.")

    # Create a yagmail.SMTP instance with the OAuth2 credentials
    yag = yagmail.SMTP(oauth2_file=TOKEN_JSON)
    return yag


def send_df_as_email(df, recipient_email):
    """
    Sends a DataFrame as an HTML email to the specified recipient.
    """
    # Authenticate and get the yagmail SMTP client
    yag = authenticate_gmail()

    # Convert DataFrame to HTML
    df_html = df.to_html()

    # Email content
    subject = "Your TopN YouTube Search Results"
    body = "Here are your DataFrame results:\n\n" + df_html

    # Send the email
    yag.send(to=recipient_email, subject=subject, contents=body)
    print(f"Email sent to {recipient_email}")


if __name__ == "__main__":
    # Test the function (you can remove this part in production)
    data = {
        'title': ['Video1', 'Video2', 'Video3'],
        'view_count': [100, 200, 300]
    }
    df = pd.DataFrame(data)
    test_email = 'leeperross@gmail.com'
    send_df_as_email(df, test_email)
