import logging
import random
from datetime import datetime

from flask import Blueprint, jsonify, current_app, request
from sqlalchemy.exc import IntegrityError
from helpers.currency import CurrencyHelper

from models.models import db, Item, UserItem

user_api = Blueprint("user_api", __name__)


# Route to get all items
@user_api.route("/collection", methods=["GET"])
def get_items():
    items = Item.query.all()
    if items:
        return jsonify([item.serialize() for item in items]), 200


# Route to get a specific item by ID
@user_api.route("/item/<int:item_id>", methods=["GET"])
def get_item_by_id(item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.serialize()), 200
    else:
        return jsonify({"message": "Item not found"}), 404


def _serialize_user_collection(user_item_joined):
    return {
        "instance_id": user_item_joined.instance_id,
        "item_id": user_item_joined.item.item_id,
        "rarity": user_item_joined.item.rarity,
        "name": user_item_joined.item.name,
        "image_path": user_item_joined.item.image_path,
        "date_roll": user_item_joined.date_roll,
    }


# Route: Visualizzare la collezione di un utente
@user_api.route("/user/<int:user_id>/collection", methods=["GET"])
def get_user_collection(user_id):
    user_item_joined = (
        db.session.query(UserItem)
        .join(Item)
        .filter_by(UserItem.user_id == user_id)
        .all()
    )

    if user_item_joined:
        return (
            jsonify(
                {
                    [
                        _serialize_user_collection(user_item)
                        for user_item in user_item_joined
                    ]
                }
            ),
            200,
        )


# Route: Ottenere informazioni su una specifica istanza della collezione di un utente
@user_api.route("/user/<int:user_id>/instance/<int:instance_id>", methods=["GET"])
def get_user_item_instance(user_id, instance_id):
    user_item_joined = (
        db.session.query(UserItem)
        .join(Item)
        .filter_by(UserItem.user_id == user_id, UserItem.instance_id == instance_id)
        .first()
    )

    if user_item_joined:
        return jsonify(_serialize_user_collection(user_item_joined)), 200
    else:
        return jsonify({"message": "Item instance not found"}), 404


@user_api.route("/user/<int:user_id>/instance/<int:instance_id>", methods=["POST"])
def move_instance(user_id, instance_id):
    new_user_id = request.json.get("new_user_id")

    if not new_user_id:
        return jsonify({"message": "New User id is mandatory"}), 400

    user_item = UserItem.query.filter_by(user_id=user_id, instance_id=instance_id).first()
    user_item.user_id = new_user_id
    db.session.commit()
    return jsonify({}), 200


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
        rarity_percentage = current_app.config["rarities"].get(rarity, 0)
        count_of_rarity = rarity_counts.get(
            rarity, 1
        )  # Default a 1 se non ci sono item di quella rarità

        # La probabilità di ciascun item è la percentuale di rarità divisa per il numero di item con quella rarità
        item_probability = rarity_percentage / count_of_rarity
        item_probabilities.append((item, item_probability))

    return item_probabilities


# Route: Roll per un nuovo gacha
@user_api.route("/user/<int:user_id>/roll", methods=["PUT"])
def roll_gacha(user_id):
    item_probabilities = _get_item_probabilities()  # Ottieni le probabilità calcolate

    if not item_probabilities:
        return jsonify({"message": "No items available for gacha"}), 404

    # Estrazione casuale di un item basato sulle probabilità calcolate
    items, probabilities = zip(*item_probabilities)
    rolled_item = random.choices(items, probabilities, k=1)[0]
    response = CurrencyHelper().sub_amount(user_id, current_app.config["roll_price"])

    if response.status_code == 200:
        new_user_item = UserItem(
            item_id=rolled_item.item_id, user_id=user_id, date_roll=datetime.utcnow()
        )
        try:
            db.session.add(new_user_item)
            db.session.commit()
            response_data = rolled_item.serialize()
            response_data["instance_id"] = new_user_item.instance_id
            return {"instance_id"}, 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Error while rolling gacha: {str(e)}")
            return jsonify({"message": "An error occurred during roll"}), 400

    return response.json(), response.status_code
