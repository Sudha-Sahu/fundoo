from flask import request, session, render_template
from mongoengine import ValidationError, NotUniqueError
from flask_restful import Resource
import json
from model import User
import jwt
from util import send_email, get_token, token_required, login_essential
import os
from dotenv import load_dotenv
load_dotenv()


class UserRegistration(Resource):
    def post(self):
        data = json.loads(request.data)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        user_name = data.get('user_name')
        password = data.get('password')
        conf_password = data.get('conf_password')
        email = data.get('email')
        gender = data.get('gender')
        session['logged in '] = False
        if conf_password != password:
            return {'error': 'password did not matched'}
        try:
            new_user = User(user_name=user_name,
                            password=password,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            gender=gender)
            new_user.save()
            token = get_token(new_user.id, new_user.user_name)
            url = f'http://127.0.0.1:9090//activate?token={token}'
            email = new_user.email
            msg = f'Hello {new_user.user_name} your account is created successfully. ' \
                  f'Now you need to activate your account by clicking the link ahead.... {url}'
            template_ = render_template(os.getenv('bodycontent'))
            send_email(email, template_)
        except ValidationError as e:
            return {'error': e.to_dict()}
        except NotUniqueError as e:
            return {'error': str(e)}

        # return {'msg': 'new user added successfully', 'token_activate_url': url}


class LoginUser(Resource):
    def get(self):
        try:
            data = request.args
            user_name = data.get('user_name')
            password = data.get('password')
            new_user = User.objects.get(user_name=user_name)
            if not new_user:
                return {'error': 'user not found'}
            if not new_user.is_active:
                token = get_token(new_user.id, new_user.user_name)
                url = f'http://127.0.0.1:9090//activate?token={token}'
                return {'error': 'user You have to verify email, verify it by clicking the link below....',
                        'token_activate_url': url}
            if password != new_user.password:
                return {'error': 'password not matching'}
            token = get_token(new_user.id, new_user.user_name)
            new_user.save()
            return {'msg': 'you are logged in....', 'token': token}
        except Exception:
            return {'error': 'Token is expired, Please login again', 'status code': 400}


class LogoutUser(Resource):
    def get(self):
        user_id = session['id']
        session['logged_in'] = False
        print(user_id, "logged out")
        return {'msg': 'Logged Out', 'code': 200}


class ActivateAccount(Resource):
    @token_required
    def get(self):
        try:
            token = request.args.get('token')
            print('token', token)
            decode_ = jwt.decode(token, "secret", algorithms=["HS256"])
            new_user = User.objects.get(id=decode_.get('user_id'))
            new_user.is_active = True
            new_user.save()
            return {'msg': 'Hi user your account is successfully activated!!!!'}
        except Exception as e:
            return {'error': "you are getting wrong token, login again to generate right token"}


class ForgetPassword(Resource):
    def post(self):
        try:
            user_id = request.form.get('user_id')
            data = User.objects(id=user_id).first()
            if not data:
                return {'message': 'User id not found!!'}
            email = data.email
            name = data.user_name
            print(f'{user_id} has been forgotten their password')
            token = get_token(data.id, name)
            url = f'http://127.0.0.1:9090//resetpassword/?token={token}'
            msg = f'Hello {name} click here to reset yor password....{url}'
            send_email(email, msg)
            data.save()
            return {'msg': 'Check your Registered Mail ID to set new Password....'}
        except Exception :
            return {'error': 'Token is missing or expired', 'status code': 400}


class ResetPassword(Resource):
    def post(self):
        try:
            user_name = request.form.get('user_name')
            data = User.objects(user_name=user_name).first()
            new_password = request.form.get('new_password')
            conf_new_password = request.form.get('conf_new_password')
            if new_password == conf_new_password:
                data.password = new_password
                print(f'{user_name} changed his password')
                data.save()
                return {'msg': 'Your new Password is Updated.'}
            else:
                return {'error': 'Re-Entered Password must be equal to New_Password'}
        except ValueError:
            return {'error': 'please enter right input', 'status code': 400}
