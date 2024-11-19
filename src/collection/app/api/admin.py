import logging

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError

from models.models import Item, db, UserItem

admin_api = Blueprint("admin_api", __name__)


# Route to get all items
@admin_api.route("/admin/<int:admin_id>/collection", methods=["GET"])
def get_items(admin_id):
    items = Item.query.all()
    if items:
        return jsonify([item.serialize() for item in items]), 200


# Route to get a specific item by ID
@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["GET"])
def get_item_by_id(admin_id, item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.serialize()), 200
    else:
        return jsonify({"message": "Item not found"}), 404


def _check_rarity(rarity):
    rarities = current_app.config["rarities"].keys()
    if rarity not in rarities:
        return jsonify({"message": f"rarity {rarity} not permitted"}), 400
    return


@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["POST"])
def update_item(admin_id, item_id):
    image_path = request.json.get("image_path")
    name = request.json.get("name")
    rarity = request.json.get("rarity")

    if not image_path and not name and not rarity:
        return jsonify({"message": "There are no fields to update"}), 400

    if rarity:
        _check_rarity(rarity)

    item = Item.query.get(item_id)
    if item:
        try:
            item.image_path = image_path if image_path else item.image_path
            item.name = name if name else item.name
            item.rarity = rarity if rarity else item.rarity
            db.session.commit()
            return jsonify(item.serialize()), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while update item: {str(e)}")
            return jsonify({"message": "An error occurred during item update"}), 400
    else:
        return jsonify({"message": "Item not found"}), 404


@admin_api.route("/admin/<int:admin_id>/item/", methods=["PUT"])
def add_item(admin_id):
    image_path = request.json.get("image_path")
    name = request.json.get("name")
    rarity = request.json.get("rarity")

    if image_path is not None and name is not None and rarity is not None:
        return jsonify({"message": "Missing mandatory fields"}), 400

    _check_rarity(rarity)

    item = Item(image_path=image_path, name=name, rarity=rarity)

    try:
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize()), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error while add gacha: {str(e)}")
        return jsonify({"message": "An error occurred while add gacha"}), 400


@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["DELETE"])
def delete_item(admin_id, item_id):
    item = Item.query.get(item_id)
    if item:
        user_items = Item.query.filter(item_id=item_id).all()
        if len(user_items) > 0:
            return (
                jsonify(
                    {
                        "message": "It is not possible to delete an item if it is present in a user's collection"
                    }
                ),
                400,
            )
        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while delete gacha: {str(e)}")
            return jsonify({"message": "An error occurred while delete gacha"}), 400

    else:
        return jsonify({"message": "Item not found"}), 404
