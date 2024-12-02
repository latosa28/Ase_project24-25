from utils_helpers.http_client import HttpClient
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from errors.errors import HTTPBadRequestError


admin_account_bp = Blueprint('admin_account', __name__)

URL = "https://admin_account:5006"


# Route to create a new account
@admin_account_bp.route('/admin', methods=['POST'])
def create_account():
    response = HttpClient.post(URL + '/admin', json=request.get_json())
    return response.json(), response.status_code


@admin_account_bp.route('/admin/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    response = HttpClient.delete(URL + f'/admin/{admin_id}', headers=request.headers)

    if response.status_code == 200:
        return jsonify({'message': 'Account deleted successfully'}), 200
    else:
        raise HTTPBadRequestError("Failed to delete account!")


@admin_account_bp.route('/admin/<int:admin_id>', methods=['GET'])
def get_admin_by_id(admin_id):
    response = HttpClient.get(URL + f'/admin/{admin_id}', headers=request.headers)
    return response.json(), response.status_code


    


