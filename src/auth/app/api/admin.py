import requests
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from helpers.token_helper import admin_token_required, generate_token_response

admin_api = Blueprint("admin_api", __name__)


ADMIN_ACCOUNT_URL = "http://admin_account:5006"


@admin_api.route('/admin/auth', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password') or not data.get('grant_type'):
        return jsonify({'error': 'invalid_request'}), 400

    username = data['username']
    password = data['password']
    grant_type = data['grant_type']

    if grant_type != 'password':
        return jsonify({'message': 'unsupported_grant_type'}), 400

    response = requests.get(ADMIN_ACCOUNT_URL + f'/admin/username/{username}')  # Account service

    if response.status_code != 200:
        return jsonify({'message': 'invalid_grant'}), 400

    admin = response.json()

    if not check_password_hash(admin['password'], password):
        return jsonify({'message': 'invalid_grant'}), 400

    token_response = generate_token_response(admin["admin_id"])

    return jsonify(token_response), 200


# Endpoint to logout (POST request to invalidate the token on the client-side)
@admin_api.route('/admin/<int:admin_id>/auth', methods=['DELETE'])
@admin_token_required
def logout(admin_id):
    return jsonify({'message': 'Successfully logged out!'}), 200
