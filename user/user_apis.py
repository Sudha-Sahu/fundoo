from flask import request, session, render_template
from mongoengine import ValidationError, NotUniqueError
from flask_restful import Resource
import json
from .model import User
from .util import send_email, get_token, token_required, decoded_token
from dotenv import load_dotenv
from .validators import validate_login
from .task import send_mail
import jwt
load_dotenv()


class LoginAPI(Resource):
    """
        This API is used to authenticate user to access resources
        @param request: user credential like username and password
        @return: Returns success message and access token on successful login
    """
    def get(self):
        data = request.args
        user_name = data.get('user_name')
        password = data.get('password')
        print(data)
        new_user = User.objects.get(user_name=user_name)
        print(new_user)
        if not new_user:
            return {'error': 'user not found'}
        if not new_user.is_active:
            token = jwt.encode({"user_id": new_user.id}, "secret", algorithm="HS256")
            url = f'http://127.0.0.1:9090//activate?token={token}'
            return {'msg': 'Activate your account', 'AccountActivationLink': url}
        if password != new_user.password:
            return {'error': 'password not matching'}
        token = jwt.encode({"user_id": new_user.id}, "secret", algorithm="HS256")
        decode_ = jwt.decode(token, "secret", algorithms=["HS256"])
        print('decoded', decode_)
        return {'msg': 'you are logged in....', 'token': token, 'status code': 200}


class UserRegistration(Resource):
    """
        This api is for user registration for userlogin project
        @param request: user registration data like username, email, password
        @return: account verification link to registered email once registration is successful
    """
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
            token = get_token(new_user.id)
            url = f'http://127.0.0.1:9090//activate?token={token}'
            email = new_user.email
            template_ = render_template('email_form.html', data=url)
            send_email(email, template_)
        except ValidationError as e:
            return {'error': e.to_dict()}
        except NotUniqueError as e:
            return {'error': str(e)}

        return {'msg': 'new user added successfully', 'token_activate_url': url}


class LoginUser(Resource):
    def post(self):
        """
        This API is used to authenticate user to access resources
        @param request: user credential like username and password
        @return: Returns success message and access token on successful login
        """
        body = {}
        req_data = request.data
        data = json.loads(req_data)
        print(data)

        body['user_name'] = data.get('user_name')
        body['password'] = data.get('password')
        validate_data = validate_login(body)
        print(validate_data['user_id'])
        # new_user = User.objects.get(user_name=user_name, password=password)
        if 'Error' in validate_data:
            return {'data': validate_data}
        if 'Error_active' in validate_data:
            token = get_token(validate_data['user_id'])
            token_url = r"http://127.0.0.1:9090/activate?token=" + f"{token}"
            template = render_template('index.html', data=token_url)
            send_mail(template, validate_data['email'])
            return {'message': 'Your account is not active activate it before login and for activation check your '
                               'mail id', 'code': 200}
        token = get_token(validate_data['user_id'])
        session.clear()
        session['logged_in'] = True
        session['user_id'] = validate_data['user_id']
        return {'message': 'logged_in', 'token': token}


class LogoutUser(Resource):
    """
        Api clear all data in session
        :return: message for logged out
    """
    def get(self):
        user_id = session['id']
        session['logged_in'] = False
        print(user_id, "logged out")
        return {'msg': 'Logged Out', 'code': 200}


class ActivateAccount(Resource):
    """
        This Api verifies the user-id and jwt token sent to the email and activates the account
        @param request: Get request hits with jwt token which contains user information
        @return: Account activation confirmation
    """
    @token_required
    def get(self):
        try:
            token = request.args.get('token')
            print('token', token)
            decode_ = decoded_token(token)
            new_user = User.objects.get(id=decode_.get('user_id'))
            new_user.is_active = True
            new_user.save()
            return {'msg': 'Hi user your account is successfully activated!!!!'}
        except Exception as e:
            return {'error': "you are getting wrong token, login again to generate right token"}


class ForgetPassword(Resource):
    """
        This API accepts get request from the email on clicked on link
        @param : email and token
        @return: success message
    """
    @token_required
    def post(self, current_user):
        try:
            data = User.objects(id=current_user.user_id).first()
            if not data:
                return {'message': 'User id not found!!'}
            email = data.email
            print(f'{current_user.user_id} has been forgotten their password')
            token = get_token(data.id)
            url = f'http://127.0.0.1:9090//resetpassword/?token={token}'
            template = render_template('email_form.html', data=url)
            send_email(email, template)
            data.save()
            return {'msg': 'Check your Registered Mail ID to set new Password....'}
        except Exception:
            return {'error': 'Token is missing or expired', 'status code': 400}


class ResetPassword(Resource):
    """
        This API accepts changes in current password
        @param : current password and new password
        @return: success message for updating the password to new password
    """
    @token_required
    def post(self, current_user):
        try:
            data = User.objects(user_name=current_user.user_name).first()
            new_password = request.form.get('new_password')
            conf_new_password = request.form.get('conf_new_password')
            if new_password == conf_new_password:
                data.password = new_password
                print(f'{current_user.user_name} changed his password')
                data.save()
                return {'msg': 'Your new Password is Updated.'}
            else:
                return {'error': 'Re-Entered Password must be equal to New_Password'}
        except ValueError:
            return {'error': 'please enter right input', 'status code': 400}
