import requests
from flask import Blueprint, request

auth_bp = Blueprint('authentication', __name__)

URL = "http://auth:5011"


@auth_bp.route('/user/auth', methods=['POST'])
def login():
    response = requests.post(f'{URL}/user/auth', json=request.get_json())
    return response.json(), response.status_code


@auth_bp.route('/user/<int:user_id>/auth', methods=['DELETE'])
def logout(user_id):
    response = requests.delete(f'{URL}/user/{user_id}/auth', headers=request.headers)
    return response.json(), response.status_code


