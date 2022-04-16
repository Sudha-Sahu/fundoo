
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import smtplib
from dotenv import load_dotenv
load_dotenv()


def send_mail(bodyContent, email):
    EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
    EMAIL_PASS = os.environ.get('EMAIL_PASS')

    msg = MIMEMultipart()
    msg['Subject'] = 'Activate Account'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.attach(MIMEText(bodyContent, "html"))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
        smtp.send_message(msg)
