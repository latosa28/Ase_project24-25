import datetime
import uuid
from functools import wraps

import jwt
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import request, jsonify

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

MY_APP = "http://localhost"


def decode_token(token):
    decoded_token = jwt.decode(
        token,
        public_key,
        algorithms=["RS256"],
        audience=MY_APP,
        issuer=MY_APP,
    )
    return decoded_token


def generate_token_response(user_id):
    # Define the token payload with standard OAuth claims
    payload = {
        "iss": MY_APP,  # Issuer: your auth server's URL
        "sub": str(user_id),  # Subject: the user's unique ID
        "aud": MY_APP,  # Audience: the API/service you're securing
        "iat": datetime.datetime.now(datetime.UTC),  # Issued at: current time
        "exp": datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(hours=1),  # Expiration time
        "scope": "all",  # Scopes: permissions granted to this token
        "jti": str(uuid.uuid4()),  # JWT ID: unique identifier for the token
    }
    # Generate the access token
    access_token = jwt.encode(payload, private_key, algorithm="RS256")
    return {"access_token": access_token, "token_type": "Bearer"}


def get_token_user_id():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return (
            jsonify({"error": "invalid_request", "error_description": "Missing token"}),
            400,
        )

    token = auth_header.removeprefix("Bearer ").strip()

    try:
        data = decode_token(token)
        token_user_id = data["sub"]
    except Exception:
        return (
            jsonify({"error": "invalid_token", "error_description": "Invalid Token"}),
            401,
        )
    return token_user_id


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_user_id = get_token_user_id()
        user_id = kwargs.get("user_id")
        if int(token_user_id) != user_id:
            return (
                jsonify(
                    {
                        "error": "insufficient_scope",
                        "error_description": "Unauthorized Access",
                    }
                ),
                403,
            )

        return f(*args, **kwargs)

    return wrapper


def admin_token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token_user_id = get_token_user_id()
        user_id = kwargs.get("admin_id")
        if int(token_user_id) != user_id:
            return jsonify({"message": "Unauthorized Access"}), 403

        return f(*args, **kwargs)

    return wrapper
