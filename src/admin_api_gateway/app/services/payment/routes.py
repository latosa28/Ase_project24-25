from utils_helpers.http_client import HttpClient
from flask import Blueprint, request

payment_bp = Blueprint('payment', __name__)

URL = "https://payment:5007"


@payment_bp.route("/admin/<int:admin_id>/user/<int:user_id>/currency_history", methods=["GET"])
def get_currency_history(admin_id, user_id):
    response = HttpClient.get(f'{URL}/admin/{admin_id}/user/{user_id}/currency_history', headers=request.headers)
    return response.json(), response.status_code
