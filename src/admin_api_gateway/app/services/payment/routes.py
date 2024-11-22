import requests
from flask import Blueprint, request

payment_bp = Blueprint('payment', __name__)

URL = "http://payment:5007"


@payment_bp.route("/admin/<int:admin_id>/user/<int:user_id>/currency_history", methods=["GET"])
def get_currency_history(admin_id, user_id):
    response = requests.get(f'{URL}/admin/{admin_id}/user/{user_id}/currency_history', headers=request.headers)
    return response.json(), response.status_code
