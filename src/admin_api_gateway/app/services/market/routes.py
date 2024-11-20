import requests
from flask import Blueprint, jsonify, request

from utils.auth import token_required

market_bp = Blueprint('market', __name__)

URL = "http://market:5004"


@market_bp.route('/admin/<int:admin_id>/market_list', methods=['GET'])
@token_required
def get_market_list(admin_id):
    response = requests.get(URL + f'/admin/<int:admin_id>/market_list')
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/user/<int:user_id>/transactions_history', methods=['GET'])
@token_required
def get_user_transactions_history(admin_id, user_id):
    response = requests.get(URL + f'/admin/{admin_id}/user/{user_id}/transactions_history')
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/transactions_history', methods=['GET'])
@token_required
def get_transactions_history(admin_id):
    response = requests.get(URL + f'/admin/{admin_id}/transactions_history')
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/market/<int:market_id>', methods=['PUT'])
@token_required
def get_auction(admin_id, market_id):
    response = requests.put(URL + f'/admin/{admin_id}/market/{market_id}', json=request.get_json())
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/market/<int:market_id>', methods=['PUT'])
@token_required
def cancel_auction(admin_id, market_id):
    response = requests.put(URL + f'/admin/{admin_id}/market/{market_id}', json=request.get_json())
    return response.json(), response.status_code
