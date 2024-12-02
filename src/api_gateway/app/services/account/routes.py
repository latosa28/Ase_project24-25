from utils_helpers.http_client import HttpClient
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from errors.errors import HTTPBadRequestError


account_bp = Blueprint('account', __name__)

URL = "https://account:5003"


# Route to create a new account
@account_bp.route('/user', methods=['POST'])
def create_account():
    response = HttpClient.post(URL + '/user', json=request.get_json())
    return response.json(), response.status_code


@account_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    response = HttpClient.delete(URL + f'/user/{user_id}', headers=request.headers)
    return response.json(), response.status_code


@account_bp.route('/user', methods=['GET'])
def get_user_by_id(current_user_id):
    response = HttpClient.get(URL + f'/user/{current_user_id}')
    return response.json(), response.status_code




