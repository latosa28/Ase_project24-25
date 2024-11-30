import logging
from utils_helpers.http_client import HttpClient
from flask import Blueprint, request


collection_bp = Blueprint('collection', __name__)

URL = "https://collection:5002"


# Route to get all items
@collection_bp.route('/admin/<int:admin_id>/collection', methods=['GET'])
def get_items(admin_id):
    response = HttpClient.get(URL + f'/admin/{admin_id}/collection', headers=request.headers)
    return response.json(), response.status_code


# Route to get a specific item by ID
@collection_bp.route('/admin/<int:admin_id>/item/<int:item_id>', methods=['GET'])
def get_item_by_id(admin_id, item_id):
    response = HttpClient.get(f'{URL}/admin/{admin_id}/item/{item_id}', headers=request.headers)
    return response.json(), response.status_code


# Route per aggiornare un item
@collection_bp.route('/admin/<int:admin_id>/item/<int:item_id>', methods=['POST'])
def update_item(admin_id, item_id):
    response = HttpClient.post(f'{URL}/admin/{admin_id}/item/{item_id}', json=request.get_json(), headers=request.headers)
    return response.json(), response.status_code


# Route per inserire un item
@collection_bp.route('/admin/<int:admin_id>/item/', methods=['PUT'])
def add_item(admin_id):
    response = HttpClient.put(f'{URL}/admin/{admin_id}/item/', json=request.get_json(), headers=request.headers)
    return response.json(), response.status_code


@collection_bp.route('/admin/<int:admin_id>/item/<int:item_id>', methods=['DELETE'])
def delete_item(admin_id, item_id):
    response = HttpClient.get(f'{URL}/admin/{admin_id}/item/{item_id}', headers=request.headers)
    return response.json(), response.status_code
