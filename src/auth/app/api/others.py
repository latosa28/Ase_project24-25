import base64

from flask import jsonify, Blueprint

from helpers.token_helper import public_key


others_api = Blueprint("others_api", __name__)


# Funzione per codificare in Base64 URL
def base64url_encode(data):
    # Converte un oggetto di tipo int in bytes, quindi codifica in base64 URL
    if isinstance(data, int):
        # Trova la lunghezza in byte necessaria per rappresentare l'intero
        length = (data.bit_length() + 7) // 8
        data = data.to_bytes(length, 'big')  # Converte l'int in bytes

    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')


@others_api.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
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