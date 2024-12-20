from utils_helpers.http_client import HttpClient
from flask import Blueprint, request

collection_bp = Blueprint('collection', __name__)

URL = "https://collection:5002"


@collection_bp.route('/user/<int:user_id>/collection', methods=['GET'])
def get_items(user_id):
    response = HttpClient.get(URL + f'/user/{user_id}/collection', headers=request.headers)
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/user/<int:user_id>/item/<int:item_id>', methods=['GET'])
def get_item_by_id(user_id, item_id):
    response = HttpClient.get(URL + f'/user/{user_id}/item/{item_id}', headers=request.headers)
    return response.json(), response.status_code


# Route per visualizzare la collezione dell'utente
@collection_bp.route('/user/<int:user_id>/mycollection', methods=['GET'])
def get_user_collection(user_id):
    response = HttpClient.get(f"{URL}/user/{user_id}/mycollection", headers=request.headers)
    return response.json(), response.status_code


# Route per ottenere informazioni su una specifica istanza di un item della collezione dell'utente
@collection_bp.route('/user/<int:user_id>/instance/<int:id_istance>', methods=['GET'])
def get_user_item_instance(user_id, id_istance):
    response = HttpClient.get(f"{URL}/user/{user_id}/instance/{id_istance}", headers=request.headers)
    return response.json(), response.status_code


# Route per effettuare un "roll" di gacha
@collection_bp.route('/user/<int:user_id>/roll', methods=['PUT'])
def roll_gacha(user_id):
    response = HttpClient.put(f"{URL}/user/{user_id}/roll", headers=request.headers)
    return response.json(), response.status_code
    