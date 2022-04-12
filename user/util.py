import os
import smtplib
import email.message
from functools import wraps
from flask import session, request, url_for, render_template
import jwt
from dotenv import load_dotenv
import datetime
from model import User
load_dotenv()


def send_email(mail, template):
    sender_address = os.environ.get("email_addr")
    sender_pass = os.environ.get("email_pass")
    receiver_address = mail
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()

    email_content = template

    msg = email.message.Message()
    msg['Subject'] = 'Email Activation'
    msg['From'] = sender_address
    msg['To'] = 'mrinalrajput3@gmail.com'
    password = sender_pass
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(email_content)

    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    server.sendmail(msg['From'], [msg['To']], msg.as_string())
    print('Mail Sent')


def get_token(user_id, user_name):
    token = jwt.encode({'user_id': user_id, 'user_name': user_name, 'Exp': str(datetime.datetime.utcnow() + datetime.timedelta(seconds=1000))},
                       os.environ.get('SECRET_KEY'), algorithm="HS256")
    return token


def token_required(func):
    @wraps(func)
    def user_decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
        if not token:
            return {'message': 'Token is missing!', 'code': 409}
        try:
            data = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=["HS256"])
            current_user = User.objects(user_name=data.user_name).first()
        except Exception as e:
            return {'message': 'token is invalid', 'code': 409}

        return func(current_user, *args, **kwargs)
    return user_decorator



#send_email('sudhasahu52@gmail.com', temp)
#get_token(31, "Dhaiya Kumar")
"""
def login_essential(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session['logged_in']:
            return {'Error': 'You have to login first'}
        return f(*args, **kwargs)
    return decorated
"""
