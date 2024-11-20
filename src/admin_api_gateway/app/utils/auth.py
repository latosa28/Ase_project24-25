from flask import request, jsonify
import jwt
from functools import wraps

# Secret key for JWT encoding and decoding (deve essere lo stesso in tutti i microservizi)
SECRET_KEY = 'mysecretkey'


# Funzione per validare il token
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        # Controlla se il token è presente nell'header Authorization
        if 'X-Auth-Token' in request.headers:
            token = request.headers['X-Auth-Token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Decodifica il token per ottenere i dati dell'utente
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_admin_id = data['admin_id']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_admin_id, *args, **kwargs)
    return decorator
