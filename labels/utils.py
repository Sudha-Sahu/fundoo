from functools import wraps
from flask import request
import jwt
from dotenv import load_dotenv

load_dotenv()


def decoded_token(token):
    data = jwt.decode(token, 'secret', algorithms=["HS256"])
    return data


def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
        else:
            token = request.args.get('token')
        if not token:
            return {'msg': 'Token is missing!', 'code': 409}
        try:
            data = decoded_token(token)
        except Exception:
            return {'msg': 'token is invalid', 'code': 409}

        return func({'_id': data['user_id']}, *args, **kwargs)
    return decorator
