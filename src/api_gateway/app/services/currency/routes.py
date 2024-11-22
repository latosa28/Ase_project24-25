import requests
from flask import Blueprint, request


currency_bp = Blueprint('currency', __name__)

URL = "http://currency:5005"


@currency_bp.route('/user/<int:user_id>/amount', methods=['GET'])
def get_amount(user_id):
    response = requests.get(f'{URL}/user/{user_id}/amount', headers=request.headers)
    return response.json(), response.status_code
