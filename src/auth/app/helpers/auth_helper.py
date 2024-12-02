import datetime
import uuid
import jwt
from utils_helpers.http_client import HttpClient
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import current_app, jsonify
from errors.errors import HTTPBadRequestError


private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

MY_APP = "https://localhost"


class AuthHelper:

    def __init__(self, role):
        self.role = role
        self.role_dict = {
            "user": (current_app.config["account"], "user_id"),
            "admin": (current_app.config["admin_account"], "admin_id"),
        }

    def mock_account_request(self, username):
        """
        Mocka la richiesta a /{account}/user/username/{username}/check_credentials.
        """
        if username == "test_user":
            return type(
                "MockResponse",
                (object,),
                {
                    "status_code": 200,
                    "json": lambda username: {"user_id": 1},
                },
            )()
        else:
            return type(
                "MockResponse",
                (object,),
                {
                    "status_code": 404,
                    "json": lambda username: {"error": "User not found"},
                },
            )()

    def mock_get_userinfo_request(self, user_id):

        return type(
            "MockResponse",
            (object,),
            {
                "status_code": 200,
                "json": lambda user: {
                    "user_id": 1,
                    "username": "test_user",
                    "email": "test_user@example.com",
                },
            },
        )()

    def do_login(self, data):
        required_fields = ["username", "password", "grant_type"]
        for field in required_fields:
            if not data.get(field):
                raise HTTPBadRequestError(f"Missing {field} field", "invalid_request")

        username = data["username"]
        password = data["password"]
        grant_type = data["grant_type"]

        if grant_type != "password":
            raise HTTPBadRequestError(
                f"grant_type {grant_type} not supported", "unsupported_grant_type"
            )

        if current_app.config["ENV"] == "testing":
            response = self.mock_account_request(username)
        else:
            response = HttpClient.post(
                self.role_dict[self.role][0]
                + f"/{self.role}/username/{username}/check_credentials",
                json={"password": password},
            )

        if response.status_code != 200:
            if response.status_code == 429:
                raise HTTPBadRequestError(
                    response.json()["error_description"], "invalid_grant"
                )
            raise HTTPBadRequestError("Not valid credentials", "invalid_grant")

        user = response.json()
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
        if current_app.config["ENV"] == "testing":
            response = self.mock_get_userinfo_request(user_id)
        else:
            response = HttpClient.get(
                self.role_dict[self.role][0] + f"/{self.role}/{user_id}"
            )

        if response.status_code != 200:
            raise HTTPBadRequestError("User not found", "invalid_request")

        data = response.json()
        return {"sub": str(user_id), **data}, 200
