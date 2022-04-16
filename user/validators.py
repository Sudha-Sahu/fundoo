from .model import User
from flask import session


def validate_login(body):
    try:
        user_name = body.get('user_name')
        password = body.get('password')
        data = User.objects.filter(user_name=user_name, password=password).first()
        if not data:
            return {'msg': "data not found"}
        if not data.is_active:
            return {'Error_active': 'your account is not activate yet check your registered mail id to activate account',
                    'email': f'{data.email}', 'user_id': data.id}
        return {'data': body, 'user_id': data.id}
    except Exception:
        return {'msg': "not able to validate"}
