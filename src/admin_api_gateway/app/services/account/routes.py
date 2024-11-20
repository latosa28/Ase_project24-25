import requests
from flask import Blueprint, request

from utils.auth import token_required

account_bp = Blueprint('account', __name__)

URL = "http://account:5003"


@account_bp.route('/admin/users', methods=['GET'])
@token_required
def get_all_users(current_admin):
    response = requests.get(URL + '/admin/users')
    return response.json(), response.status_code


@account_bp.route('/admin/<int:admin_id>/user/<int:user_id>', methods=['POST'])
@token_required
def modify_user(current_admin, admin_id, user_id):
    response = requests.post(URL + f'/admin/{admin_id}/user/{user_id}', json=request.get_json())
    return response.json(), response.status_code
