from flask import Blueprint, jsonify, request
from helpers.auth_helper import AuthHelper
from helpers.token_helper import token_authorized, get_token_info

user_api = Blueprint("user_api", __name__)


@user_api.route("/user/auth", methods=["POST"])
def login():
    data = request.get_json()
    return AuthHelper('user').do_login(data)


@user_api.route("/userinfo", methods=["GET"])
def userinfo():
    user_id = get_token_info()
    return AuthHelper('user').get_userinfo(user_id)


# Endpoint to logout (POST request to invalidate the token on the client-side)
@user_api.route("/user/<int:user_id>/auth", methods=["DELETE"])
@token_authorized
def logout(user_id):
    return jsonify({"message": "Successfully logged out"}), 200


