import logging

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError

from errors.errors import HTTPNotFoundError, HTTPBadRequestError, HTTPInternalServerError
from utils_helpers.token import admin_token_authorized
from models.models import Item, db, UserItem
from utils_helpers.validation import get_body_field

admin_api = Blueprint("admin_api", __name__)


# Route to get all items
@admin_api.route("/admin/<int:admin_id>/collection", methods=["GET"])
@admin_token_authorized
def get_items(admin_id):
    items = Item.query.all()
    if items:
        return jsonify([item.serialize() for item in items]), 200


# Route to get a specific item by ID
@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["GET"])
@admin_token_authorized
def get_item_by_id(admin_id, item_id):
    item = Item.query.get(item_id)
    if item:
        return jsonify(item.serialize()), 200
    else:
        raise HTTPNotFoundError("Item not found")


def _check_rarity(rarity):
    rarities = current_app.config["rarities"].keys()
    if rarity not in rarities:
        raise HTTPBadRequestError(f"rarity {rarity} not permitted")


@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["POST"])
@admin_token_authorized
def update_item(admin_id, item_id):
    image_path = get_body_field("image_path")
    name = get_body_field("name")
    rarity = get_body_field("rarity")

    if not image_path and not name and not rarity:
        raise HTTPNotFoundError("There are no fields to update")

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
            logging.error(f"Error while updating item: {str(e)}")
            raise HTTPInternalServerError()
    else:
        raise HTTPNotFoundError("Item not found")


@admin_api.route("/admin/<int:admin_id>/item/", methods=["PUT"])
@admin_token_authorized
def add_item(admin_id):
    image_path = get_body_field("image_path")
    name = get_body_field("name")
    rarity = get_body_field("rarity")

    if not image_path or not name or not rarity:
        raise HTTPBadRequestError("Missing mandatory fields")
    _check_rarity(rarity)
    item = Item(image_path=image_path, name=name, rarity=rarity)

    try:
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize()), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error while adding item: {str(e)}")
        raise HTTPInternalServerError()


@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["DELETE"])
@admin_token_authorized
def delete_item(admin_id, item_id):
    item = Item.query.get(item_id)
    if not item:
        raise HTTPNotFoundError("Item not found")

    first_user_item = UserItem.query.filter_by(item_id=item_id).first()
    if first_user_item:
        raise HTTPBadRequestError("It is not possible to delete an item if it's present in a user's collection")
    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "item deleted successfully"}), 200
    except Exception:
        db.session.rollback()
        raise HTTPInternalServerError()



