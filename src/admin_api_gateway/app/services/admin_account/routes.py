import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from errors.errors import HTTPBadRequestError


admin_account_bp = Blueprint('admin_account', __name__)

URL = "http://admin_account:5006"


# Route to create a new account
@admin_account_bp.route('/admin', methods=['POST'])
def create_account():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        raise HTTPBadRequestError("Missing required fields!")

    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'], method='pbkdf2:sha256')

    # Send request to account service to create the user
    response = requests.post(URL + '/admin', json={
        'username': username,
        'email': email,
        'password': password
    })

    if response.status_code == 201:
        response_data = response.json()
        admin_id = response_data.get('admin_id')

        if admin_id:
            return jsonify({
                'message': 'Account created successfully!'
            }), 201
        else:
            raise HTTPBadRequestError("Failed to retrieve user_id!")
    else:
        raise HTTPBadRequestError("Failed to create account!")


@admin_account_bp.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    response = requests.delete(URL + f'/admin/{admin_id}', headers=request.headers)

    if response.status_code == 200:
        return jsonify({'message': 'Account deleted successfully'}), 200
    else:
        raise HTTPBadRequestError("Failed to delete account!")


@admin_account_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin_by_id(admin_id):
    response = requests.get(URL + f'/admin/{admin_id}', headers=request.headers)
    return response.json(), response.status_code


    


