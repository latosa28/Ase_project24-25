import requests
from flask import Blueprint
from utils.auth import token_required

payment_bp = Blueprint('payment', __name__)

URL = "http://payment:5007"


@payment_bp.route("/admin/<int:admin_id>/user/<int:user_id>/currency_history", methods=["GET"])
@token_required
def get_currency_history(user, admin_id, user_id):
    response = requests.get(f'{URL}/admin/{admin_id}/user/{user_id}/currency_history')
    return response.json(), response.status_code
