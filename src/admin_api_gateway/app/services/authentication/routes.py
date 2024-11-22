import requests
from flask import Blueprint, request

auth_bp = Blueprint('authentication', __name__)

URL = "http://auth:5011"


@auth_bp.route('/admin/auth', methods=['POST'])
def login():
    response = requests.post(f'{URL}/admin/auth', json=request.get_json())
    return response.json(), response.status_code


@auth_bp.route('/admin/<int:admin_id>/auth', methods=['DELETE'])
def logout(admin_id):
    response = requests.delete(f'{URL}/admin/{admin_id}/auth', headers=request.headers)
    return response.json(), response.status_code
