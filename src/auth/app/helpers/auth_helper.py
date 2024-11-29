import datetime
import uuid
import jwt
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import request, jsonify
from werkzeug.security import check_password_hash
from errors.errors import HTTPBadRequestError

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

MY_APP = "http://localhost"
ACCOUNT_URL = "http://account:5003"
ADMIN_ACCOUNT_URL = "http://admin_account:5006"


class AuthHelper:
    role_dict = {
        "user": (ACCOUNT_URL, "user_id"),
        "admin": (ADMIN_ACCOUNT_URL, "admin_id"),
    }

    def __init__(self, role):
        self.role = role

    def do_login(self, data):
        if (
            not data
            or not data.get("username")
            or not data.get("password")
            or not data.get("grant_type")
        ):
            raise HTTPBadRequestError("Missing mandatory fields", "invalid_request")

        username = data["username"]
        password = data["password"]
        grant_type = data["grant_type"]

        if grant_type != "password":
            raise HTTPBadRequestError(f"grant_type {grant_type} not supported", "unsupported_grant_type")

        response = requests.get(
            self.role_dict[self.role][0] + f"/{self.role}/username/{username}"
        )

        if response.status_code != 200:
            raise HTTPBadRequestError("Not valid credentials", "invalid_grant")

        user = response.json()

        if not check_password_hash(user["password"], password):
            raise HTTPBadRequestError("Not valid credentials", "invalid_grant")

        token_response = self.generate_token_response(
            user[self.role_dict[self.role][1]]
        )

        return jsonify(token_response), 200

    def generate_token_response(self, user_id):
        # Define the token payload with standard OAuth claims
        payload = {
            "iss": MY_APP,  # Issuer: your auth server's URL
            "sub": str(user_id),  # Subject: the user's unique ID
            "aud": MY_APP,  # Audience: the API/service you're securing
            "iat": datetime.datetime.now(datetime.UTC),  # Issued at: current time
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(hours=1),  # Expiration time
            "scope": self.role,  # Scopes: permissions granted to this token
            "jti": str(uuid.uuid4()),  # JWT ID: unique identifier for the token
        }
        # Generate the access token
        access_token = jwt.encode(payload, private_key, algorithm="RS256")
        return {"access_token": access_token, "token_type": "Bearer"}

    def get_userinfo(self, user_id):
        response = requests.get(
            self.role_dict[self.role][0] + f"/{self.role}/{user_id}"
        )
        if response.status_code != 200:
            raise HTTPBadRequestError("User not found", "invalid_request",)

        data = response.json()
        return {"sub": str(user_id), **data}, 200
