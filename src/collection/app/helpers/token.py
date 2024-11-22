from functools import wraps
import jwt
from flask import request, jsonify, current_app

MY_APP = "http://localhost"


def decode_token(token, public_key):
    decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=MY_APP,
        issuer=MY_APP,
    )
    return decoded_token


def get_token_user_id():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'message': 'Token is missing!'}), 403

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        data = decode_token(token, current_app.config["jwt_public_key"])
        token_user_id = data['sub']
        return token_user_id
    except Exception:
        return jsonify({'message': 'Token is invalid!'}), 403


def token_authorized(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.config['ENV'] == 'testing':
            return f(*args, **kwargs)
        token_user_id = get_token_user_id()
        user_id = kwargs.get('user_id')
        if int(token_user_id) != user_id:
            return jsonify({'message': 'Unauthorized Access'}), 403

        return f(*args, **kwargs)
    return decorator


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.config['ENV'] == 'testing':
            return f(*args, **kwargs)
        get_token_user_id()
        return f(*args, **kwargs)
    return decorator


def admin_token_authorized(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if current_app.config['ENV'] == 'testing':
            return f(*args, **kwargs)
        token_user_id = get_token_user_id()
        user_id = kwargs.get('admin_id')
        if int(token_user_id) != user_id:
            return jsonify({'message': 'Unauthorized Access'}), 403

        return f(*args, **kwargs)
    return decorator


