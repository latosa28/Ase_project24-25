import logging
import requests
from flask import Blueprint, jsonify, request
from utils.auth import token_required

collection_bp = Blueprint('collection', __name__)

URL = "http://collection:5002"


# Route to get all items
@collection_bp.route('/admin/collection', methods=['GET'])
@token_required
def get_items(current_admin_id):
    response = requests.get(URL + f'/admin/{current_admin_id}/collection')
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/admin/item/<int:item_id>', methods=['GET'])
@token_required
def get_item_by_id(current_admin_id, item_id):
    response = requests.get(URL + f'/admin/{current_admin_id}/item/{item_id}')
    return response.json(), response.status_code


# Route per aggiornare un item
@collection_bp.route('/admin/item/<int:item_id>', methods=['POST'])
@token_required
def update_item(current_admin_id, item_id):
    # Recupera i dati dal corpo della richiesta
    image_path = request.json.get("image_path")
    name = request.json.get("name")
    rarity = request.json.get("rarity")

    # Verifica che almeno un campo sia presente
    if not image_path and not name and not rarity:
        return jsonify({"message": "There are no fields to update"}), 400

    # Invia i dati al microservizio remoto
    try:
        response = requests.post(
            f"{URL}/admin/{current_admin_id}/item/{item_id}",
            json={"image_path": image_path, "name": name, "rarity": rarity},
        )
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the item service: {str(e)}")
        return jsonify({"message": "Failed to update item due to a communication error"}), 500



# Route per inserire un item
@collection_bp.route('/admin/item/', methods=['PUT'])
@token_required
def add_item(current_admin_id):
    # Recupera i dati dal corpo della richiesta
    image_path = request.json.get("image_path")
    name = request.json.get("name")
    rarity = request.json.get("rarity")

    # Verifica che tutti i campi obbligatori siano presenti
    if not image_path or not name or not rarity:
        return jsonify({"message": "Missing mandatory fields"}), 400

    # Invia i dati al microservizio remoto
    try:
        response = requests.put(
            f"{URL}/admin/{current_admin_id}/item/",
            json={"image_path": image_path, "name": name, "rarity": rarity},
        )
        return response.json(), response.status_code
    except requests.RequestException as e:
        logging.error(f"Error communicating with the item service: {str(e)}")
        return jsonify({"message": "Failed to add item due to a communication error"}), 500




@collection_bp.route('/admin/item/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(current_admin_id, item_id):
    try:
        response = requests.delete(f"{URL}/admin/{current_admin_id}/item/{item_id}")
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        logging.error(f"Error while calling the microservice: {str(e)}")
        return jsonify({"message": "Failed to connect to the item microservice"}), 500
