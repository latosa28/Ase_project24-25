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
    response = requests.get(f'{URL}/admin/{current_admin_id}/collection')
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/admin/item/<int:item_id>', methods=['GET'])
@token_required
def get_item_by_id(current_admin_id, item_id):
    response = requests.get(f'{URL}/admin/{current_admin_id}/item/{item_id}')
    return response.json(), response.status_code


# Route per aggiornare un item
@collection_bp.route('/admin/item/<int:item_id>', methods=['POST'])
@token_required
def update_item(current_admin_id, item_id):
    response = requests.post(f'{URL}/admin/{current_admin_id}/item/{item_id}', json=request.get_json())
    return response.json(), response.status_code


# Route per inserire un item
@collection_bp.route('/admin/item/', methods=['PUT'])
@token_required
def add_item(current_admin_id):
    response = requests.put(f'{URL}/admin/{current_admin_id}/item/', json=request.get_json())
    return response.json(), response.status_code


@collection_bp.route('/admin/item/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(current_admin_id, item_id):
    response = requests.get(f'{URL}/admin/{current_admin_id}/item/{item_id}')
    return response.json(), response.status_code
