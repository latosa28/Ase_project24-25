import requests
from flask import Blueprint, request, jsonify
from utils.auth import token_required

currency_bp = Blueprint('currency', __name__)

URL = "http://currency:5005"


@currency_bp.route('/user/<int:user_id>/amount', methods=['GET'])
@token_required
def get_amount(user, user_id):
    response = requests.get(f'{URL}/user/{user_id}/amount')
    return response.json(), response.status_code
