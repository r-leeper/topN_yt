import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('EMAIL_PASSWORD')
sender = os.getenv('EMAIL_ADDRESS')


def send_df_as_email(df_to_send, recipient_email):
    """
    Sends a DataFrame as an HTML email to the specified recipient.
    """



    # Convert DataFrame to HTML
    df_html = df_to_send.to_html()

    # Email content
    subject = "Your TopN YouTube Search Results"
    body = "Here are your DataFrame results:\n\n" + df_html

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'html'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender, password)  # Log in
            server.send_message(msg)  # Send the email
            print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')


if __name__ == "__main__":
    # Test the function (you can remove this part in production)
    data = {
        'title': ['Video1', 'Video2', 'Video3'],
        'view_count': [100, 200, 300]
    }
    df = pd.DataFrame(data)
    test_email = 'leeperross@gmail.com'
    send_df_as_email(df, test_email)
