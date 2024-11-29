import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from errors.errors import HTTPBadRequestError


account_bp = Blueprint('account', __name__)

URL = "http://account:5003"


# Route to create a new account
@account_bp.route('/user', methods=['POST'])
def create_account():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        raise HTTPBadRequestError("Missing required fields!")

    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Send request to account service to create the user
    response = requests.post(URL + '/user', json={
        'username': username,
        'email': email,
        'password': password
    })
    return response.json(), response.status_code


@account_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = requests.delete(URL + f'/user/{user_id}',headers=request.headers)
    return response.json(), response.status_code


@account_bp.route('/user', methods=['GET'])
def get_user_by_id(current_user_id):
    response = requests.get(URL + f'/user/{current_user_id}')
    return response.json(), response.status_code




