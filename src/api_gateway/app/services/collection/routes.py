import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.utils.auth import token_required

collection_bp = Blueprint('collection', __name__)

URL = "http://collection:5002"


# Route to create a new item (pokemon)
@collection_bp.route('/item', methods=['POST'])
def create_item():
    data = request.get_json()

    if not data or not data.get('rarity') or not data.get('characteristics'):
        return jsonify({'message': 'Missing required fields!'}), 400

    rarity = data['rarity']
    characteristics = data['characteristics']

    # Send request to collection service to create the item
    response = requests.post(URL + '/item', json={
        'rarity': rarity,
        'characteristics': characteristics
    })

    if response.status_code == 201:
        return jsonify({'message': 'Item created successfully!'}), 201
    else:
        return jsonify({'message': 'Failed to create item!'}), 400


# Route to get all items
@collection_bp.route('/collection', methods=['GET'])
@token_required
def get_items(current_user):
    response = requests.get(URL + '/collection')
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/item/<int:id_item>', methods=['GET'])
@token_required
def get_item_by_id(current_user,id_item):
    response = requests.get(URL + f'/item/{id_item}')
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
    