import requests
from flask import Blueprint, request, jsonify
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from utils.auth import token_required

auth_bp = Blueprint('authentication', __name__)

ACCOUNT_URL = "http://account:5003"


# login
@auth_bp.route('/user/auth', methods=['POST'])
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
    token = jwt.encode({
        'user_id': user["user_id"],
        'exp': datetime.utcnow() + timedelta(hours=1)
    }, 'mysecretkey', algorithm="HS256")

    return jsonify({'token': token})


# Endpoint to logout (POST request to invalidate the token on the client-side)
@auth_bp.route('/user/auth', methods=['DELETE'])
@token_required
def logout(current_user):
    # Invalidate the token on the client side (simple approach)
    return jsonify({'message': 'Successfully logged out!'}), 200