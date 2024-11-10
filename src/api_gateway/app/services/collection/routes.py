from flask import Blueprint, jsonify

from api_gateway.app.utils.auth import token_required

collection_bp = Blueprint('collection', __name__)


# Route for collection data (example)
@collection_bp.route('/get_items', methods=['GET'])
@token_required  # Applica il decorator per validare il token
def get_items(current_user):
    # Simulazione di una risposta dal database o da un altro servizio
    items = [{"id": 1, "name": "Item1"}, {"id": 2, "name": "Item2"}]
    return jsonify(items)
