import json
import requests
from flask import current_app
from jwt.algorithms import RSAAlgorithm

AUTH_URL = "http://auth:5011"


class AuthHelper:

    @staticmethod
    def get_jwt_public_key(env):
        jwks = None

        if env == 'testing':
            return ""

        response = requests.get(f"{AUTH_URL}/.well-known/jwks.json")

        if response.status_code == 200:
            jwks = response.json()

        if not jwks:
            raise Exception("Errore nel recupero delle chiavi JWK")

        key = jwks['keys'][0]
        if key['kty'] != 'RSA':
            raise ValueError("Chiave non RSA, impossibile costruire la chiave pubblica.")
        public_key = RSAAlgorithm.from_jwk(json.dumps(key))
        return public_key
