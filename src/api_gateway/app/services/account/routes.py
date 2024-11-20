import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from utils.auth import token_required

account_bp = Blueprint('account', __name__)

URL = "http://account:5003"


# Route to create a new account
@account_bp.route('/user', methods=['POST'])
def create_account():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields!'}), 400

    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Send request to account service to create the user
    response = requests.post(URL + '/user', json={
        'username': username,
        'email': email,
        'password': password
    })

    if response.status_code == 201:
        response_data = response.json()
        user_id = response_data.get('user_id')

        if user_id:
            return jsonify({
                'message': 'Account created successfully!'
            }), 201
        else:
            return jsonify({'message': 'Failed to retrieve user_id!'}), 400
    else:
        return jsonify({'message': 'Failed to create account!'}), 400


@account_bp.route('/user', methods=['DELETE'])
@token_required
def delete_user(current_user_id):
    response = requests.delete(URL + f'/user/{current_user_id}')

    if response.status_code == 200:
        return jsonify({'message': 'Account deleted successfully'}), 200
    else:
        return jsonify({'message': 'Failed to delete account!'}), 400


@account_bp.route('/user', methods=['GET'])
@token_required
def get_user_by_id(current_user_id):
    response = requests.get(URL + f'/user/{current_user_id}')
    return response.json(), response.status_code




