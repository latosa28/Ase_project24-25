import requests
from flask import Blueprint, request
from utils.auth import token_required

payment_bp = Blueprint('payment', __name__)

URL = "http://payment:5007"


@payment_bp.route('/user/payment', methods=['POST'])
@token_required
def pay(current_user_id):
    response = requests.post(f'{URL}/user/{current_user_id}/payment', json=request.get_json())
    return response.json(), response.status_code
