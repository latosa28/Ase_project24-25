import logging
import requests
from flask import Blueprint, jsonify, request

from utils.auth import token_required

market_bp = Blueprint('market', __name__)

URL = "http://market:5004"


@market_bp.route('/admin/<int:admin_id>/market_list', methods=['GET'])
@token_required
def get_market_list(current_admin, admin_id):
    try:
        # Effettua la richiesta al microservizio
        response = requests.get(f"{URL}/admin/{admin_id}/market_list")
        
        # Restituisce la risposta del microservizio
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the market service: {str(e)}")
        return jsonify({"message": "Failed to retrieve market list due to a communication error"}), 500



@market_bp.route('/admin/<int:admin_id>/user/<int:user_id>/transactions_history', methods=['GET'])
@token_required
def get_user_transactions_history(current_admin, admin_id, user_id):
    try:
        # Effettua la richiesta al microservizio
        response = requests.get(f"{URL}/admin/{admin_id}/user/{user_id}/transactions_history")

        # Restituisce la risposta del microservizio
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the transaction history service: {str(e)}")
        return jsonify({"message": "Failed to retrieve transaction history due to a communication error"}), 500



@market_bp.route('/admin/<int:admin_id>/transactions_history', methods=['GET'])
@token_required
def get_transactions_history(current_admin, admin_id):
    try:
        # Effettua la richiesta al microservizio
        response = requests.get(f"{URL}/admin/{admin_id}/transactions_history")

        # Restituisce la risposta del microservizio
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the transaction history service: {str(e)}")
        return jsonify({"message": "Failed to retrieve transaction history due to a communication error"}), 500



@market_bp.route('/admin/<int:admin_id>/market/<int:market_id>', methods=['GET'])
@token_required
def get_auction(current_admin, admin_id, market_id):
    try:
        # Effettua una richiesta GET al microservizio
        response = requests.get(f"{URL}/admin/{admin_id}/market/{market_id}")

        # Restituisce la risposta del microservizio
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the auction service: {str(e)}")
        return jsonify({"message": "Failed to retrieve auction due to a communication error"}), 500



@market_bp.route('/admin/<int:admin_id>/market/<int:market_id>', methods=['POST'])
@token_required
def cancel_auction(current_admin, admin_id, market_id):
    try:
        # Effettua una richiesta POST al microservizio
        response = requests.post(f"{URL}/admin/{admin_id}/market/{market_id}")

        # Restituisce la risposta del microservizio
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the auction service: {str(e)}")
        return jsonify({"message": "Failed to cancel auction due to a communication error"}), 500

