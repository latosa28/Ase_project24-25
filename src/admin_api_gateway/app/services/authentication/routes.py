from utils_helpers.http_client import HttpClient
from flask import Blueprint, request

auth_bp = Blueprint('authentication', __name__)

URL = "https://auth:5011"


@auth_bp.route('/admin/auth', methods=['POST'])
def login():
    response = HttpClient.post(f'{URL}/admin/auth', json=request.get_json())
    return response.json(), response.status_code


@auth_bp.route('/userinfo', methods=['GET'])
def userinfo():
    response = HttpClient.get(f'{URL}/admin/userinfo', headers=request.headers)
    return response.json(), response.status_code


@auth_bp.route('/admin/<int:admin_id>/auth', methods=['DELETE'])
def logout(admin_id):
    response = HttpClient.delete(f'{URL}/admin/{admin_id}/auth', headers=request.headers)
    return response.json(), response.status_code
