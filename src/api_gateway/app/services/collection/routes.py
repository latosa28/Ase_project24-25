import requests
from flask import Blueprint
from utils.auth import token_required

collection_bp = Blueprint('collection', __name__)

URL = "http://collection:5002"


@collection_bp.route('/collection', methods=['GET'])
@token_required
def get_items(current_user):
    response = requests.get(URL + '/collection')
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/item/<int:item_id>', methods=['GET'])
@token_required
def get_item_by_id(current_user, item_id):
    response = requests.get(URL + f'/item/{item_id}')
    return response.json(), response.status_code


# Route per visualizzare la collezione dell'utente
@collection_bp.route('/user/<int:user_id>/collection', methods=['GET'])
@token_required
def get_user_collection(current_user,user_id):
    response = requests.get(f"{URL}/user/{user_id}/collection")
    return response.json(), response.status_code


# Route per ottenere informazioni su una specifica istanza di un item della collezione dell'utente
@collection_bp.route('/user/<int:user_id>/instance/<int:id_istance>', methods=['GET'])
@token_required
def get_user_item_instance(current_user,user_id, id_istance):
    response = requests.get(f"{URL}/user/{user_id}/instance/{id_istance}")
    return response.json(), response.status_code


# Route per effettuare un "roll" di gacha
@collection_bp.route('/user/<int:user_id>/roll', methods=['PUT'])
@token_required
def roll_gacha(current_user,user_id):
    response = requests.put(f"{URL}/user/{user_id}/roll")
    return response.json(), response.status_code
    