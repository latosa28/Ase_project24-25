import base64
import logging
import requests
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash

from helpers.token_helper import generate_token, token_required, public_key

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
ACCOUNT_URL = "http://account:5003"


@app.route('/user/auth', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password!'}), 400

    username = data['username']
    password = data['password']

    response = requests.get(ACCOUNT_URL + f'/user/username/{username}')  # Account service

    if response.status_code != 200:
        return jsonify({'message': 'User not found!'}), 404

    user = response.json()

    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid password!'}), 401

    # Genera il JWT token
    token = generate_token(user["user_id"])

    return jsonify({'token': token})


# Endpoint to logout (POST request to invalidate the token on the client-side)
@app.route('/user/<int:user_id>/auth', methods=['DELETE'])
@token_required
def logout(user_id):
    return jsonify({'message': 'Successfully logged out!'}), 200


# Funzione per codificare in Base64 URL
def base64url_encode(data):
    # Converte un oggetto di tipo int in bytes, quindi codifica in base64 URL
    if isinstance(data, int):
        # Trova la lunghezza in byte necessaria per rappresentare l'intero
        length = (data.bit_length() + 7) // 8
        data = data.to_bytes(length, 'big')  # Converte l'int in bytes

    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

# Crea l'endpoint JWK per esporre la chiave pubblica
@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    # Ritorna la chiave pubblica in formato JWK
    jwk = {
        "keys": [
            {
                "kty": "RSA",  # Tipo di chiave
                "kid": "1",    # ID della chiave (puoi scegliere un valore che abbia senso)
                "use": "sig",  # Tipo di utilizzo, in questo caso firma (sig)
                "alg": "RS256",  # Algoritmo di firma
                "n": base64url_encode(public_key.public_numbers().n),  # Modulo della chiave pubblica
                "e": base64url_encode(public_key.public_numbers().e),  # Esponente pubblico
            }
        ]
    }
    return jsonify(jwk)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010)
