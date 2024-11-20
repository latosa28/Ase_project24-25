import requests
from flask import Blueprint, jsonify, request

from utils.auth import token_required

market_bp = Blueprint('market', __name__)

URL = "http://market:5004"


@market_bp.route('/market_list', methods=['GET'])
@token_required
def get_market_list(current_user_id):
    response = requests.get(URL + f'/market_list')
    return response.json(), response.status_code


@market_bp.route('/user/transactions_history', methods=['GET'])
@token_required
def get_transactions_history(current_user_id):
    response = requests.get(URL + f'/user/{current_user_id}/transactions_history')
    return response.json(), response.status_code


@market_bp.route('/user/market/<int:market_id>/bid', methods=['PUT'])
@token_required
def place_bid(current_user_id, market_id):
    response = requests.put(URL + f'/user/{current_user_id}/market/{market_id}/bid', json=request.get_json())
    return response.json(), response.status_code


@market_bp.route('/user/instance/<int:instance_id>/auction', methods=['PUT'])
@token_required
def set_auction(curren_user_id, instance_id):
    response = requests.put(URL + f'/user/{curren_user_id}/instance/{instance_id}/auction', json=request.get_json())
    return response.json(), response.status_code
