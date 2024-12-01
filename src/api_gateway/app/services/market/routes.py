from utils_helpers.http_client import HttpClient
from flask import Blueprint, request


market_bp = Blueprint('market', __name__)

URL = "https://market:5004"


@market_bp.route('/user/<int:user_id>/market_list', methods=['GET'])
def get_market_list(user_id):
    response = HttpClient.get(URL + f'/user/{user_id}/market_list', headers=request.headers)
    return response.json(), response.status_code


@market_bp.route('/user/<int:user_id>/transactions_history', methods=['GET'])
def get_transactions_history(user_id):
    response = HttpClient.get(URL + f'/user/{user_id}/transactions_history', headers=request.headers)
    return response.json(), response.status_code


@market_bp.route('/user/<int:user_id>/market/<int:market_id>/bid', methods=['PUT'])
def place_bid(user_id, market_id):
    response = HttpClient.put(URL + f'/user/{user_id}/market/{market_id}/bid', headers=request.headers, json=request.get_json())
    return response.json(), response.status_code


@market_bp.route('/user/<int:user_id>/instance/<int:instance_id>/auction', methods=['PUT'])
def set_auction(user_id, instance_id):
    response = HttpClient.put(URL + f'/user/{user_id}/instance/{instance_id}/auction', headers=request.headers, json=request.get_json())
    return response.json(), response.status_code
