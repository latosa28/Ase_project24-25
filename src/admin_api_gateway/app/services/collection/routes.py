import requests
from flask import Blueprint
from utils.auth import token_required

collection_bp = Blueprint('collection', __name__)

URL = "http://collection:5002"


# Route to get all items
@collection_bp.route('/admin/<int:admin_id>/collection', methods=['GET'])
@token_required
def get_items(current_user, admin_id):
    response = requests.get(URL + f'/admin/{admin_id}/collection')
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/admin/<int:admin_id>/item/<int:item_id>', methods=['GET'])
@token_required
def get_item_by_id(current_user,admin_id, item_id):
    response = requests.get(URL + f'/admin/{admin_id}/item/{item_id}')
    return response.json(), response.status_code


# Route per aggiornare un item della collezione dell'utente
@collection_bp.route('/admin/<int:admin_id>/item/<int:item_id>', methods=['POST'])
@token_required
def update_item(current_user,admin_id,item_id):
    response = requests.get(URL + f'/admin/{admin_id}/item/{item_id}')
    return response.json(), response.status_code


# Route per aggiungere un item alla collezione dell'utente
@collection_bp.route('/admin/<int:admin_id>/item/', methods=['PUT'])
@token_required
def add_item(current_user,admin_id):
    response = requests.get(URL + f'/admin/{admin_id}/item/')
    return response.json(), response.status_code


# Route per eliminare un item dalla collezione dell'utente
@collection_bp.route('/admin/<int:admin_id>/item/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user,admin_id, item_id):
    response = requests.put(URL + f'/admin/{admin_id}/item/{item_id}')
    return response.json(), response.status_code
    