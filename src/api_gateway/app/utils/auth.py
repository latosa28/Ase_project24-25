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
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Ottieni il token dal formato "Bearer <token>"

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # Decodifica il token per ottenere i dati dell'utente
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = data['username']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    return decorator
