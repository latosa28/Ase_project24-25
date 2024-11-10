import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash


account_bp = Blueprint('account', __name__)


# Route to create a new account
@account_bp.route('/create', methods=['POST'])
def create_account():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields!'}), 400

    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'], method='sha256')

    # Send request to account service to create the user
    response = requests.post('http://account:5003/create', json={
        'username': username,
        'email': email,
        'password': password
    })

    if response.status_code == 201:
        return jsonify({'message': 'Account created successfully!'}), 201
    else:
        return jsonify({'message': 'Failed to create account!'}), 400
