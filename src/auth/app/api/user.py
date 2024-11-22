import base64

import requests
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from helpers.token_helper import public_key, generate_token, token_required

user_api = Blueprint("user_api", __name__)

ACCOUNT_URL = "http://account:5003"


@user_api.route('/user/auth', methods=['POST'])
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
@user_api.route('/user/<int:user_id>/auth', methods=['DELETE'])
@token_required
def logout(user_id):
    return jsonify({'message': 'Successfully logged out!'}), 200





