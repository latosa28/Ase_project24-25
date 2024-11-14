import requests
from flask import Blueprint, jsonify, request

from app.utils.auth import token_required

market_bp = Blueprint('market', __name__)

URL = "http://market:5004"


@market_bp.route('/user/<int:user_id>/market_list', methods=['GET'])
@token_required
def get_market_list(user, user_id):
    response = requests.get(URL + f'/user/{user_id}/market_list')
    return response.json(), response.status_code


@market_bp.route('/user/<int:user_id>/transactions_history', methods=['GET'])
@token_required
def get_transactions_history(user, user_id):
    response = requests.get(URL + f'/user/{user_id}/transactions_history')
    return response.json(), response.status_code


@market_bp.route('/user/<int:user_id>/market/<int:market_id>/bid', methods=['PUT'])
@token_required
def place_bid(user, user_id, market_id):
    response = requests.put(URL + f'/user/{user_id}/market/{market_id}/bid', json=request.get_json())
    return response.json(), response.status_code


@market_bp.route('/user/<int:user_id>/instance/<int:instance_id>/auction', methods=['PUT'])
@token_required
def set_auction(user, user_id, instance_id):
    response = requests.put(URL + f'/user/{user_id}/instance/{instance_id}/auction', json=request.get_json())
    return response.json(), response.status_code
