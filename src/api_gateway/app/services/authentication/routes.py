import requests
from flask import Blueprint, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from api_gateway.app.utils.auth import token_required

auth_bp = Blueprint('authentication', __name__)


# login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password!'}), 400

    username = data['username']
    password = data['password']

    # Verifica il nome utente e la password (simulazione)
    response = requests.get(f'http://account:5003/get_user/{username}')  # Account service

    if response.status_code != 200:
        return jsonify({'message': 'User not found!'}), 404

    user = response.json()

    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid password!'}), 401

    # Genera il JWT token
    token = jwt.encode({
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, 'mysecretkey', algorithm="HS256")

    return jsonify({'token': token})


# Endpoint to logout (POST request to invalidate the token on the client-side)
@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(user_id):
    # Invalidate the token on the client side (simple approach)
    return jsonify({'message': 'Successfully logged out!'}), 200