from fundoo.user.apis import UserRegistration, LogoutUser, ResetPassword, ForgetPassword, LoginUser, ActivateAccount

user_routes = [
    (LoginUser, '/login/'),
    (UserRegistration, '/register/'),
    (ActivateAccount, '/activate/'),
    (ForgetPassword, '/forgetpassword/'),
    (LogoutUser, '/logout/'),
    (ResetPassword, '/resetpassword/')
]


"""

from flask import Flask, request, session
from mongoengine import ValidationError, NotUniqueError
from flask_restful import Resource, Api
import json
from model import User
import jwt
from util import send mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'af6263f9c9984fd78fb242775905d95f'
api = Api(app)


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
            token = jwt.encode({"user_id": new_user.id, 'user_name': new_user.user_name}, "secret", algorithm="HS256")
            url = f'http://127.0.0.1:9090//activate?token={token}'
            activate_my_email(email, url, new_user.id)
        except ValidationError as e:
            return {'error': e.to_dict()}
        except NotUniqueError as e:
            return {'error': str(e)}

        return {'msg': 'new user added successfully', 'token_activate_url': url}


class LoginUser(Resource):
    def get(self):
        data = request.args
        user_name = data.get('user_name')
        password = data.get('password')
        new_user = User.objects.get(user_name=user_name)
        if not new_user:
            return {'error': 'user not found'}
        if not new_user.is_active:
            return {'error': 'You have to verify email'}
        if password != new_user.password:
            return {'error': 'password not matching'}
        token = jwt.encode({"user_id": new_user.id, 'user_name': new_user.user_name}, "secret", algorithm="HS256")
        decode_ = jwt.decode(token, "secret", algorithms=["HS256"])
        print('decoded', decode_)
        return {'msg': 'you are logged in....', 'token': token}


class LogoutUser(Resource):
    def get(self):
        user_id = session['id']
        session['logged_in'] = False
        print(user_id, "logged out")
        return {'msg': 'Logged Out', 'code': 200}


class ActivateAccount(Resource):
    def get(self):
        token = request.args.get('token')
        print('token', token)
        decode_ = jwt.decode(token, "secret", algorithms=["HS256"])
        print('decode', decode_)
        new_user = User.objects.get(id=decode_.get('user_id'))
        new_user.is_active = True
        new_user.save()
        return {'msg': 'Hi user your account is successfully activated!!!!'}


class ForgetPassword(Resource):
    def post(self):
        user_name = request.form.get('user_name')
        data = User.objects(user_name=user_name).first()
        if not data:
            return {'message': 'User name not found!!'}
        email = data.email
        name = data.user_name
        print(f'{user_name} has been forgotten their password')
        token = request.args.get('token')
        print(token)
        activate_my_email(email, )
        return {'msg': 'Check your Registered Mail ID to set new Password....'}


class ResetPassword(Resource):
    def post(self):
        if session['logged_in']:
            user_name = request.form.get('user_name')
            last_pass = request.form.get('old_password')
            new_password1 = request.form.get('new_password')
            conf_new_password = request.form.get('Re-Enter New Password')
            if new_password1 == conf_new_password:
                print(f'{user_name} changed his password')
                return {'msg': 'Your Password is Updated.'}
            else:
                return {'msg': 'Re-Entered Password must be equal to New_Password'}
        else:
            return {'msg': 'user please Login First'}


"""