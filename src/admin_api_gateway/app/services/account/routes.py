import requests
from flask import Blueprint, request

account_bp = Blueprint("account", __name__)

URL = "http://account:5003"


@account_bp.route("/admin/<int:admin_id>/users", methods=["GET"])
def get_all_users(admin_id):
    response = requests.get(URL + f"/admin/{admin_id}/users", headers=request.headers)
    return response.json(), response.status_code


@account_bp.route("/admin/<int:admin_id>/user/<int:user_id>", methods=["POST"])
def modify_user(admin_id, user_id):
    response = requests.post(
        URL + f"/admin/{admin_id}/user/{user_id}",
        json=request.get_json(),
        headers=request.headers,
    )
    return response.json(), response.status_code
