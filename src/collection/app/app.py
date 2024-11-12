import logging

import requests
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from datetime import datetime
import random

from sqlalchemy.exc import IntegrityError

from config import load_config
from models import db, Item, UserItem

# Initialize the Flask application
app = Flask(__name__)
load_config(app)
db.init_app(app)  # Qui inizializziamo il db con l'app
ma = Marshmallow(app)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

CURRENCY_URL = "http://currency:5005"


# Schema di Marshmallow per Item
class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item


# Schema di Marshmallow per UserItem
class UserItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserItem


# Crea un'istanza di schema per serializzare i dati
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
user_item_schema = UserItemSchema()
user_items_schema = UserItemSchema(many=True)


# Route to create a new item (pokemon)
# @app.route('/item', methods=['POST'])
# def create_item():
#     # Get data from the incoming JSON request
#     rarity = request.json.get('rarity')
#     characteristics = request.json.get('characteristics')
#
#     # Ensure all required fields are provided
#     if not rarity or not characteristics:
#         return jsonify({"message": "Missing data"}), 400
#
#     # Create a new item instance
#     new_item = Item(rarity=rarity, characteristics=characteristics)
#
#     try:
#         db.session.add(new_item)
#         db.session.commit()
#         return jsonify({"item_id": new_item.item_id}), 201
#     except IntegrityError:
#         db.session.rollback()
#         logging.error(f"Error while creating item: {str(e)}")
#         return jsonify({"message": "An error occurred while processing your request."}), 400


# Route to get all items
@app.route("/collection", methods=["GET"])
def get_items():
    items = Item.query.all()
    if items:
        # Return all items data as JSON
        items_data = ItemSchema(many=True).dump(items)
        return jsonify(items_data), 200
    else:
        return jsonify({"message": "No items found"}), 404


# Route to get a specific item by ID
@app.route("/item/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = Item.query.get(item_id)
    if item:
        # Return the item data as JSON
        item_data = ItemSchema().dump(item)
        return jsonify(item_data), 200
    else:
        return jsonify({"message": "Item not found"}), 404


# Route: Visualizzare la collezione di un utente
@app.route("/user/<int:user_id>/collection", methods=["GET"])
def get_user_collection(user_id):
    user_items = UserItem.query.filter_by(user_id=user_id).all()
    if user_items:
        return jsonify(user_items_schema.dump(user_items)), 200
    else:
        return jsonify({"message": "No items found in this collection"}), 404


# Route: Ottenere informazioni su una specifica istanza della collezione di un utente
@app.route("/user/<int:user_id>/instance/<int:istance_id>", methods=["GET"])
def get_user_item_instance(user_id, istance_id):
    user_item = UserItem.query.filter_by(user_id=user_id, istance_id=istance_id).first()
    if user_item:
        return jsonify(user_item_schema.dump(user_item)), 200
    else:
        return jsonify({"message": "Item instance not found"}), 404


# Funzione per calcolare le probabilità degli item
def _get_item_probabilities():
    items = Item.query.all()
    # Raggruppiamo gli item per rarità
    rarity_counts = {}
    for item in items:
        if item.rarity not in rarity_counts:
            rarity_counts[item.rarity] = 0
        rarity_counts[item.rarity] += 1

    # Calcoliamo i pesi per ogni item
    item_probabilities = []
    for item in items:
        rarity = item.rarity
        rarity_percentage = app.config["rarities"].get(rarity, 0)
        count_of_rarity = rarity_counts.get(rarity, 1)  # Default a 1 se non ci sono item di quella rarità

        # La probabilità di ciascun item è la percentuale di rarità divisa per il numero di item con quella rarità
        item_probability = rarity_percentage / count_of_rarity
        item_probabilities.append((item, item_probability))

    return item_probabilities


# Route: Roll per un nuovo gacha
@app.route("/user/<int:user_id>/roll", methods=["PUT"])
def roll_gacha(user_id):
    item_probabilities = _get_item_probabilities()  # Ottieni le probabilità calcolate

    if not item_probabilities:
        return jsonify({"message": "No items available for gacha"}), 404

    # Estrazione casuale di un item basato sulle probabilità calcolate
    items, probabilities = zip(*item_probabilities)
    rolled_item = random.choices(items, probabilities, k=1)[0]
    response = requests.post(CURRENCY_URL + f'/user/{user_id}/sub_amount', json={"amount": app.config["roll_price"]})

    if response.status_code == 200:
        new_user_item = UserItem(
            item_id=rolled_item.item_id, user_id=user_id, date_roll=datetime.utcnow()
        )
        try:
            db.session.add(new_user_item)
            db.session.commit()
            response_data = ItemSchema().dump(rolled_item)
            response_data["istance_id"] = new_user_item.istance_id
            return response_data, 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error while rolling gacha: {str(e)}")
            return jsonify({"message": "An error occurred during roll"}), 400

    return response.json(), response.status_code


# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
