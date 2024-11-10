import requests
from flask import Blueprint, jsonify, make_response
from requests import HTTPError

from app.utils.auth import token_required

collection_bp = Blueprint('collection', __name__)

URL = 'http://collection:5002'


# Route for collection data (example)
@collection_bp.route('/get_items', methods=['GET'])
def get_items():
    # Simulazione di una risposta dal database o da un altro servizio
    items = [{"id": 1, "name": "Item1"}, {"id": 2, "name": "Item2"}]
    return jsonify(items)


def string_request(URL_API):
    try:
        x = requests.get(URL_API)
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('String service is down\n', 500)
    except HTTPError:
        return make_response(x.content, x.status_code)


@collection_bp.route('/collection', methods=['GET'])
def collection():
    json_response = string_request(URL + f'/collection')
    return json_response



