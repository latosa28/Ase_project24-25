import logging
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import random

from sqlalchemy.exc import IntegrityError

# Initialize the Flask application
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Marshmallow for ORM and serialization
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Define the Item model for the 'item' table in the database
class Item(db.Model):
    id_item = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String(50), nullable=False)
    characteristics = db.Column(db.Text, nullable=False)

    def __init__(self, rarity, characteristics):
        self.rarity = rarity
        self.characteristics = characteristics

class UserItem(db.Model):
    id_istance = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer, db.ForeignKey('item.id_item'), nullable=False)
    id_user = db.Column(db.Integer, nullable=False)
    date_roll = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Schema for serializing the Item object into JSON
class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item

class UserItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserItem

item_schema = ItemSchema()
user_item_schema = UserItemSchema()
user_items_schema = UserItemSchema(many=True)

# Route to create a new item (pokemon)
@app.route('/item', methods=['POST'])
def create_item():
    # Get data from the incoming JSON request
    rarity = request.json.get('rarity')
    characteristics = request.json.get('characteristics')

    # Ensure all required fields are provided
    if not rarity or not characteristics:
        return jsonify({"message": "Missing data"}), 400

    # Create a new item instance
    new_item = Item(rarity=rarity, characteristics=characteristics)

    try:
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"id_item": new_item.id_item}), 201
    except IntegrityError:
        db.session.rollback()
        logging.error(f"Error while creating item: {str(e)}")
        return jsonify({"message": "An error occurred while processing your request."}), 400


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
@app.route('/item/<int:id_item>', methods=['GET'])
def get_item_by_id(id_item):
    item = Item.query.get(id_item)
    if item:
        # Return the item data as JSON
        item_data = ItemSchema().dump(item)
        return jsonify(item_data), 200
    else:
        return jsonify({"message": "Item not found"}), 404
    
# Route: Visualizzare la collezione di un utente
@app.route('/user/<int:user_id>/collection', methods=['GET'])
def get_user_collection(user_id):
    user_items = UserItem.query.filter_by(id_user=user_id).all()
    if user_items:
        return jsonify(user_items_schema.dump(user_items)), 200
    else:
        return jsonify({"message": "No items found in this collection"}), 404


# Route: Ottenere informazioni su una specifica istanza della collezione di un utente
@app.route('/user/<int:user_id>/instance/<int:id_istance>', methods=['GET'])
def get_user_item_instance(user_id, id_istance):
    user_item = UserItem.query.filter_by(id_user=user_id, id_istance=id_istance).first()
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
    new_user_item = UserItem(id_item=rolled_item.id_item, id_user=user_id, date_roll=datetime.utcnow())

    try:
        db.session.add(new_user_item)
        db.session.commit()
        print("Record successfully added to database")
        print(f"ID_istance generated: {new_user_item.id_istance}")
        return jsonify({
        "message": "Item added to collection",
        "id_item": rolled_item.id_item,
        "rarity": rolled_item.rarity,
        "characteristics": rolled_item.characteristics,
        "id_istance": new_user_item.id_istance
    }), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error while rolling gacha: {str(e)}")
        return jsonify({"message": "An error occurred during roll"}), 400


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
