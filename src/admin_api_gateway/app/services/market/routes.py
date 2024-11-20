import logging
import requests
from flask import Blueprint, jsonify, request

from utils.auth import token_required

market_bp = Blueprint('market', __name__)

URL = "http://market:5004"


@market_bp.route('/admin/market_list', methods=['GET'])
@token_required
def get_market_list(current_admin_id):
    response = requests.get(f"{URL}/market_list")
    return response.json(), response.status_code


@market_bp.route('/admin/user/<int:user_id>/transactions_history', methods=['GET'])
@token_required
def get_user_transactions_history(current_admin_id, user_id):
    response = requests.get(f"{URL}/admin/{current_admin_id}/user/{user_id}/transactions_history")
    return response.json(), response.status_code


@market_bp.route('/admin/transactions_history', methods=['GET'])
@token_required
def get_transactions_history(current_admin_id):
    response = requests.get(f"{URL}/admin/{current_admin_id}/transactions_history")
    return response.json(), response.status_code


@market_bp.route('/admin/market/<int:market_id>', methods=['GET'])
@token_required
def get_auction(current_admin_id, market_id):
    response = requests.get(f"{URL}/admin/{current_admin_id}/market/{market_id}")
    return response.json(), response.status_code


@market_bp.route('/admin/market/<int:market_id>', methods=['POST'])
@token_required
def cancel_auction(current_admin_id, market_id):
    response = requests.post(f"{URL}/admin/{current_admin_id}/market/{market_id}")
    return response.json(), response.status_code
