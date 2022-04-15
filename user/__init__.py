from .user_apis import UserRegistration, LogoutUser, ResetPassword, ForgetPassword, LoginUser, ActivateAccount

user_routes = [
    (LoginUser, '/login/'),
    (UserRegistration, '/register/'),
    (ActivateAccount, '/activate/'),
    (ForgetPassword, '/forgetpassword/'),
    (LogoutUser, '/logout/'),
    (ResetPassword, '/resetpassword/')
]
