import requests
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from helpers.token_helper import generate_token, admin_token_required

admin_api = Blueprint("admin_api", __name__)


ADMIN_ACCOUNT_URL = "http://admin_account:5006"


@admin_api.route('/admin/auth', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing username or password!'}), 400

    username = data['username']
    password = data['password']

    response = requests.get(ADMIN_ACCOUNT_URL + f'/admin/username/{username}')  # Account service

    if response.status_code != 200:
        return jsonify({'message': 'User not found!'}), 404

    admin = response.json()

    if not check_password_hash(admin['password'], password):
        return jsonify({'message': 'Invalid password!'}), 401

    # Genera il JWT token
    token = generate_token(admin["admin_id"])

    return jsonify({'token': token})


# Endpoint to logout (POST request to invalidate the token on the client-side)
@admin_api.route('/admin/<int:admin_id>/auth', methods=['DELETE'])
@admin_token_required
def logout(admin_id):
    return jsonify({'message': 'Successfully logged out!'}), 200
