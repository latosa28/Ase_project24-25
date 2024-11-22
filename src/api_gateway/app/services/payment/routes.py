import requests
from flask import Blueprint, request
from utils.auth import token_required

payment_bp = Blueprint('payment', __name__)

URL = "http://payment:5007"


@payment_bp.route('/user/<int:user_id>/payment', methods=['POST'])
def pay(user_id):
    response = requests.post(f'{URL}/user/{user_id}/payment',headers=request.headers, json=request.get_json())
    return response.json(), response.status_code
