import logging
from utils_helpers.http_client import HttpClient
from flask import Blueprint, request

market_bp = Blueprint('market', __name__)

URL = "https://market:5004"


@market_bp.route('/admin/<int:admin_id>/market_list', methods=['GET'])
def get_market_list(admin_id):
    response = HttpClient.get(URL + f'/admin/{admin_id}/market_list', headers=request.headers)
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/user/<int:user_id>/transactions_history', methods=['GET'])
def get_user_transactions_history(admin_id, user_id):
    response = HttpClient.get(f"{URL}/admin/{admin_id}/user/{user_id}/transactions_history", headers=request.headers)
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/transactions_history', methods=['GET'])
def get_transactions_history(admin_id):
    response = HttpClient.get(f"{URL}/admin/{admin_id}/transactions_history", headers=request.headers)
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/market/<int:market_id>', methods=['GET'])
def get_auction(admin_id, market_id):
    response = HttpClient.get(f"{URL}/admin/{admin_id}/market/{market_id}", headers=request.headers)
    return response.json(), response.status_code


@market_bp.route('/admin/<int:admin_id>/market/<int:market_id>', methods=['POST'])
def cancel_auction(admin_id, market_id):
    response = HttpClient.post(f"{URL}/admin/{admin_id}/market/{market_id}", headers=request.headers)
    return response.json(), response.status_code
