from flask import Blueprint, jsonify

from app.utils.auth import token_required

market_bp = Blueprint('market', __name__)


# Route for market data (example)
@market_bp.route('/get_market', methods=['GET'])
@token_required  # Applica il decorator per validare il token
def get_market(current_user):
    # Simulazione di una risposta dal database o da un altro servizio
    market_data = [{"id": 1, "item": "Item1", "price": "100 USD"}]
    return jsonify(market_data)
