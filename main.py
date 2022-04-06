from flask import Flask, request, session, make_response, jsonify
from mongoengine import connect, ValidationError, NotUniqueError
from flask_restful import Resource, Api
import json
from model import User
import jwt

connect(host='mongodb://127.0.0.1:27017/FlaskUserProject')

app = Flask(__name__)
api = Api(app)


class UserRegistration(Resource):
    def get(self, id_):
        data = request.args
        user_name = data.get('user_name')
        password = data.get('password')
        print('data get', id_, user_name, password)
        return {'msg': 'you are getting data successfully'}

    def post(self, id_):
        data = json.loads(request.data)
        print('body_data', data)
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
            new_user = User(user_name=user_name, password=password, first_name=first_name, last_name=last_name, email=email, gender=gender)
            new_user.save()
            token = jwt.encode({"user_id": new_user.id, 'user_name': new_user.user_name}, "secret", algorithm="HS256")
            url = f'http://127.0.0.1:9090//activate?token={token}'
            activate_my_email(email, url, user_name)
        except ValidationError as e:
            print(e.to_dict())
            return {'error': e.to_dict()}
        except NotUniqueError as e:
            print(e)
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
        print('password', new_user.password)
        print('user', new_user)
        if password != new_user.password:
            return {'error': 'password not matching'}
        token = jwt.encode({"user_id": new_user.id, 'user_name': new_user.user_name}, "secret", algorithm="HS256")
        decode_ = jwt.decode(token, "secret", algorithms=["HS256"])
        print('decoded', decode_)
        print('data get', data.get('user_name'))
        return {'msg': 'you are logged in....', 'token': token}


class LogoutUser(Resource):
    def get(self):
        user_id = session['id']
        session['logged_in'] = False
        print(user_id, "logged out")
        return make_response(jsonify(message='Logged Out'), 200)


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
        return {'msg': 'Check your Registered Mail ID to set new Password....'}


class ResetPassword(Resource):
    def post(self):
        if session['logged_in']:
            user_name = request.form.get('UserName')
            old_pass = request.form.get('Old Password')
            new_password1 = request.form.get('New Password')
            conf_password2 = request.form.get('Re-Enter New Password')
            if new_password1 == conf_password2:
                data = User.objects(user_name=user_name).first()
                if old_pass == data.password:
                    data.update(password=new_password1)
                    print(f'{user_name} changed his password')
                    return {'msg': 'Your Password is Updated.'}
                else:
                    return {'msg': 'Check Your old Password'}
            else:
                return {'msg': 'Re-Entered Password must be equal to New_Password'}
        else:
            return {'msg': 'You have to Login First'}


api.add_resource(LoginUser, '/login/')
api.add_resource(UserRegistration, '/register/<int:id_>')
api.add_resource(ActivateAccount, '/activate/')
api.add_resource(LogoutUser, '/logout/')
api.add_resource(ForgetPassword, '/forgetpassword/')
api.add_resource(ResetPassword, '/resetpassword/')

if __name__ == "__main__":
    app.run(debug=True, port=9090)

