import requests
from flask import Blueprint, request, jsonify
from app.utils.auth import token_required

currency_bp = Blueprint('currency', __name__)

# URL del microservizio currency
URL = "http://currency:5005"


@currency_bp.route('/user/<int:user_id>/amount', methods=['GET'])
@token_required
def get_amount(user, user_id):
    response = requests.get(f'{URL}/user/{user_id}/amount')
    return response.json(), response.status_code


@currency_bp.route('/user/<int:user_id>/add_amount', methods=['POST'])
@token_required
def add_amount(user, user_id):
    data = request.json
    amount_to_add = data.get("amount")

    if amount_to_add is None:
        return jsonify({"error": "Amount is required"}), 400

    response = requests.post(f'{URL}/user/{user_id}/add_amount', json={"amount": amount_to_add})
    return response.json(), response.status_code


@currency_bp.route('/user/<int:user_id>/sub_amount', methods=['POST'])
@token_required
def sub_amount(user, user_id):
    data = request.json
    amount_to_sub = data.get("amount")

    if amount_to_sub is None:
        return jsonify({"error": "Amount is required"}), 400

    response = requests.post(f'{URL}/user/{user_id}/sub_amount', json={"amount": amount_to_sub})
    return response.json(), response.status_code
