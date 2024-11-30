
from flask import Blueprint, jsonify, request
from helpers.auth_helper import AuthHelper
from helpers.token_helper import admin_token_authorized, get_token_info

admin_api = Blueprint("admin_api", __name__)


@admin_api.route('/admin/auth', methods=['POST'])
def login():
    data = request.get_json()
    return AuthHelper('admin').do_login(data)


@admin_api.route("/admin/userinfo", methods=["GET"])
def userinfo():
    admin_id = get_token_info()
    return AuthHelper('admin').get_userinfo(admin_id)


# Endpoint to logout (POST request to invalidate the token on the client-side)
@admin_api.route('/admin/<int:admin_id>/auth', methods=['DELETE'])
@admin_token_authorized
def logout(admin_id):
    return jsonify({'message': 'Successfully logged out!'}), 200
