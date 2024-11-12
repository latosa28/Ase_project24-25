import json
import logging
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
import random

from sqlalchemy.exc import IntegrityError

# Initialize the Flask application
app = Flask(__name__)


def load_rarity_config():
    # Apre il file rarity_config.json e carica i dati
    with open('/conf/rarity_conf.json', 'r') as file:
        rarity_data = json.load(file)

    # Verifica che la somma delle percentuali sia 100
    total_percentage = sum(rarity_data.values())
    if total_percentage != 100.0:
        raise ValueError(f"Le percentuali sommano {total_percentage}. Devono essere esattamente 100.")

    return rarity_data


# Carica la configurazione al momento dell'avvio dell'app
rarity_config = load_rarity_config()
logging.basicConfig(level=logging.DEBUG)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow for ORM and serialization
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define the Item model for the 'item' table in the database
class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    image_path = db.Column(db.String(255), nullable=False)

    def __init__(self, rarity, name, image_path):
        self.rarity = rarity
        self.name = name
        self.image_path = image_path


class UserItem(db.Model):
    istance_id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date_roll = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    item = db.relationship('Item', backref=db.backref('user_items', lazy=True))

    def __init__(self, item_id, user_id, date_roll):
        self.item_id = item_id
        self.user_id = user_id
        self.date_roll = date_roll

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
@app.route('/collection', methods=['GET'])
def get_items():
    items = Item.query.all()
    if items:
        # Return all items data as JSON
        items_data = ItemSchema(many=True).dump(items)
        return jsonify(items_data), 200
    else:
        return jsonify({"message": "No items found"}), 404


# Route to get a specific item by ID
@app.route('/item/<int:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    item = Item.query.get(item_id)
    if item:
        # Return the item data as JSON
        item_data = ItemSchema().dump(item)
        return jsonify(item_data), 200
    else:
        return jsonify({"message": "Item not found"}), 404


# Route: Visualizzare la collezione di un utente
@app.route('/user/<int:user_id>/collection', methods=['GET'])
def get_user_collection(user_id):
    user_items = UserItem.query.filter_by(user_id=user_id).all()
    if user_items:
        return jsonify(user_items_schema.dump(user_items)), 200
    else:
        return jsonify({"message": "No items found in this collection"}), 404


# Route: Ottenere informazioni su una specifica istanza della collezione di un utente
@app.route('/user/<int:user_id>/instance/<int:istance_id>', methods=['GET'])
def get_user_item_instance(user_id, istance_id):
    user_item = UserItem.query.filter_by(user_id=user_id, istance_id=istance_id).first()
    if user_item:
        return jsonify(user_item_schema.dump(user_item)), 200
    else:
        return jsonify({"message": "Item instance not found"}), 404


# Route: Roll per un nuovo gacha
@app.route('/user/<int:user_id>/roll', methods=['PUT'])
def roll_gacha(user_id):
    # Estrai un item casuale dal database
    items = Item.query.all()
    if not items:
        return jsonify({"message": "No items available for gacha"}), 404

    # Selezione casuale di un item
    rolled_item = random.choice(items)

    # Creazione della nuova istanza dell'item nella collezione dell'utente
    new_user_item = UserItem(item_id=rolled_item.item_id, user_id=user_id, date_roll=datetime.utcnow())

    try:
        db.session.add(new_user_item)
        db.session.commit()
        print("Record successfully added to database")
        print(f"istance_id generated: {new_user_item.istance_id}")
        return jsonify({
        "message": "Item added to collection",
        "item_id": rolled_item.item_id,
        "rarity": rolled_item.rarity,
        "name": rolled_item.name,
        "image_path": rolled_item.image_path,
        "istance_id": new_user_item.istance_id
    }), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error while rolling gacha: {str(e)}")
        return jsonify({"message": "An error occurred during roll"}), 400


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
