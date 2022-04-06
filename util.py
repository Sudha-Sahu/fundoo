import os
import smtplib
from model import User
# from template import email


def activate_my_email(email, url, id):

    email_addr = os.environ.get('email_addr')
    email_passw = os.environ.get('email_pass')

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(email_addr, email_passw)

    sender = email_addr
    receiver = email
    msg = f"Hello {User.user_name},\n Click the link to activate your account {url}"

    server.sendmail(sender, receiver, msg)

