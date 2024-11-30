from utils_helpers.http_client import HttpClient
from flask import Blueprint, request

payment_bp = Blueprint('payment', __name__)

URL = "https://payment:5007"


@payment_bp.route('/user/<int:user_id>/payment', methods=['POST'])
def pay(user_id):
    response = HttpClient.post(f'{URL}/user/{user_id}/payment',headers=request.headers, json=request.get_json())
    return response.json(), response.status_code
