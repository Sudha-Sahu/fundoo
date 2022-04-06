from routes import LoginUser, UserRegistration, ActivateAccount, LogoutUser, ForgetPassword, ResetPassword
from flask import Flask
from flask_restful import Api
from db.mydatabase import my_database

app = Flask(__name__)
api = Api(app)


api.add_resource(LoginUser, '/login/')
api.add_resource(UserRegistration, '/register/')
api.add_resource(ActivateAccount, '/activate/')
api.add_resource(LogoutUser, '/logout/')
api.add_resource(ForgetPassword, '/forgetpassword/')
api.add_resource(ResetPassword, '/resetpassword/')


if __name__ == "__main__":
    app.run(debug=True, port=9090)

