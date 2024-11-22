import requests
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from helpers.token_helper import token_required, generate_token_response

user_api = Blueprint("user_api", __name__)

ACCOUNT_URL = "http://account:5003"


@user_api.route('/user/auth', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password') or not data.get('grant_type'):
        return jsonify({'error': 'invalid_request'}), 400

    username = data['username']
    password = data['password']
    grant_type = data['grant_type']

    if grant_type != 'password':
        return jsonify({'message': 'unsupported_grant_type'}), 400

    response = requests.get(ACCOUNT_URL + f'/user/username/{username}')  # Account service

    if response.status_code != 200:
        return jsonify({'message': 'invalid_grant'}), 400

    user = response.json()

    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'invalid_grant'}), 400

    token_response = generate_token_response(user["user_id"])

    return jsonify(token_response), 200


# Endpoint to logout (POST request to invalidate the token on the client-side)
@user_api.route('/user/<int:user_id>/auth', methods=['DELETE'])
@token_required
def logout(user_id):
    return jsonify({'message': 'Successfully logged out!'}), 200





