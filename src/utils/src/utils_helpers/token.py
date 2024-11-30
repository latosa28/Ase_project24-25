from functools import wraps
import jwt
from flask import request, jsonify, current_app

from errors.errors import HTTPUnauthorizedError, HTTPForbiddenError

MY_APP = "https://localhost"


def decode_token(token, public_key):
    decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=MY_APP,
        issuer=MY_APP,
    )
    return decoded_token


def get_token_info():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Token is missing!'}), 403

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        data = decode_token(token, current_app.config["jwt_public_key"])
        token_user_id = data.get('sub')
        return token_user_id
    except Exception:
        raise HTTPUnauthorizedError("Invalid token", "invalid_token")


def token_authorized(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.config['ENV'] == 'testing':
            return f(*args, **kwargs)
        token_user_id = get_token_info()
        user_id = kwargs.get('user_id')
        if int(token_user_id) != user_id:
            raise HTTPForbiddenError("Unauthorized Access", "unauthorized")

        return f(*args, **kwargs)
    return decorator


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.config['ENV'] == 'testing':
            return f(*args, **kwargs)
        get_token_info()
        return f(*args, **kwargs)
    return decorator


def admin_token_authorized(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.config['ENV'] == 'testing':
            return f(*args, **kwargs)
        token_user_id = get_token_info()
        admin_id = kwargs.get('admin_id')
        if int(token_user_id) != admin_id:
            raise HTTPForbiddenError("Unauthorized Access", "unauthorized")

        return f(*args, **kwargs)
    return decorator


