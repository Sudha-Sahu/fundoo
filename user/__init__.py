from .user_apis import UserRegistration, LogoutUser, ResetPassword, ForgetPassword, LoginUser, ActivateAccount, LoginAPI

user_routes = [
    # (LoginUser, '/login/'),
    (UserRegistration, '/register/'),
    (ActivateAccount, '/activate/'),
    (ForgetPassword, '/forgetpassword/'),
    (LogoutUser, '/logout/'),
    (ResetPassword, '/resetpassword/'),
    (LoginAPI, '/loginapi/')
]
