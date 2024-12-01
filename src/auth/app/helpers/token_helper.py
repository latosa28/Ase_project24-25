from functools import wraps

import jwt
from flask import request

from errors.errors import HTTPBadRequestError, HTTPUnauthorizedError, HTTPForbiddenError
from helpers.auth_helper import public_key, MY_APP


def decode_token(token):
    decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=MY_APP,
        issuer=MY_APP,
    )
    return decoded_token


def get_token_info():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPBadRequestError("Missing token", "invalid_request")

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        data = decode_token(token)
        token_user_id = data["sub"]
        return token_user_id
    except Exception:
        raise HTTPUnauthorizedError("Invalid token", "invalid_token")


def token_authorized(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_user_id = get_token_info()
        user_id = kwargs.get("user_id")
        if int(token_user_id) != user_id:
            raise HTTPForbiddenError("Unauthorized Access", "unauthorized")

        return f(*args, **kwargs)
    return wrapper


def admin_token_authorized(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_admin_id = get_token_info()
        admin_id = kwargs.get("admin_id")
        if int(token_admin_id) != admin_id:
            raise HTTPForbiddenError("Unauthorized Access", "unauthorized")
        return f(*args, **kwargs)
    return wrapper
