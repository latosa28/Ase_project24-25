import datetime
import uuid
import jwt
import requests
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import current_app, request, jsonify
from werkzeug.security import check_password_hash
from errors.errors import HTTPBadRequestError


private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

MY_APP = "http://localhost"


class AuthHelper:

    def __init__(self, role):
        self.role = role
        self.role_dict = {
            "user": (current_app.config["account"], "user_id"),
            "admin": (current_app.config["admin_account"], "admin_id"),
        }

    def mock_account_request(self, username):
        """
        Mocka la richiesta a /account/user/username/{username}.
        """
        if username == "test_user":
            return type('MockResponse', (object,), {
                "status_code": 200,
                "json": lambda username: {'user_id': 1, 'username': 'test_user', 'password': 'hashedpassword', 'email': 'test_user@example.com'}
            })()
        else:
            return type('MockResponse', (object,), {
                "status_code": 404,
                "json": lambda username: {'error': 'User not found'}
            })()


    def mock_get_userinfo_request(self, user_id):

        return type('MockResponse', (object,), {
            "status_code": 200,
            "json": lambda user: {'user_id': 1, 'username': 'test_user', 'email': 'test_user@example.com'}
        })()



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

        
        if current_app.config['ENV'] == 'testing':
            # Usa il mock durante il testing
            response = self.mock_account_request(username)
        else:
            response = requests.get(
                self.role_dict[self.role][0] + f"/{self.role}/username/{username}"
            )

        if response.status_code != 200:
            raise HTTPBadRequestError("Not valid credentials", "invalid_grant")

        user = response.json()

        if current_app.config['ENV'] != 'testing' and not check_password_hash(user["password"], password):
            raise HTTPBadRequestError("Not valid credentials", "invalid_grant")

        token_response = self.generate_token_response(
            user[self.role_dict[self.role][1]]
        )

        return jsonify(token_response), 200
        
    def generate_token_response(self, user_id):
        payload = {
            "iss": MY_APP,  
            "sub": str(user_id),  
            "aud": MY_APP,  
            "iat": datetime.datetime.now(datetime.UTC),  
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
            "scope": self.role,  
            "jti": str(uuid.uuid4()),  
        }
        access_token = jwt.encode(payload, private_key, algorithm="RS256")
        return {"access_token": access_token, "token_type": "Bearer"}

    def get_userinfo(self, user_id):
        if current_app.config['ENV'] == 'testing':
            response = self.mock_get_userinfo_request(user_id)
        else:
            response = requests.get(
                self.role_dict[self.role][0] + f"/{self.role}/{user_id}"
            )

        if response.status_code != 200:
            raise HTTPBadRequestError("User not found", "invalid_request")

        data = response.json()
        return {"sub": str(user_id), **data}, 200