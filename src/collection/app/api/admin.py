import logging

from flask import Blueprint, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError

from helpers.token import admin_token_authorized
from models.models import Item, db, UserItem

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
        return jsonify({"message": "Item not found"}), 404


def _check_rarity(rarity):
    rarities = current_app.config["rarities"].keys()
    if rarity not in rarities:
        return jsonify({"message": f"rarity {rarity} not permitted"}), 400
    return


@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["POST"])
@admin_token_authorized
def update_item(admin_id, item_id):
    # Recupera i dati dal corpo della richiesta
    image_path = request.json.get("image_path")
    name = request.json.get("name")
    rarity = request.json.get("rarity")

    # Verifica che almeno un campo sia presente
    if not image_path and not name and not rarity:
        return jsonify({"message": "There are no fields to update"}), 400

    # Controlla la validità della rarità
    if rarity:
        rarity_check = _check_rarity(rarity)
        if rarity_check:
            return rarity_check  # Ritorna la risposta di errore dal controllo di rarità

    # Trova l'oggetto nel database
    item = Item.query.get(item_id)
    if item:
        try:
            # Aggiorna solo i campi forniti
            item.image_path = image_path if image_path else item.image_path
            item.name = name if name else item.name
            item.rarity = rarity if rarity else item.rarity

            # Salva le modifiche
            db.session.commit()
            return jsonify(item.serialize()), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while updating item: {str(e)}")
            return jsonify({"message": "An error occurred during item update"}), 400
    else:
        return jsonify({"message": "Item not found"}), 404


@admin_api.route("/admin/<int:admin_id>/item/", methods=["PUT"])
@admin_token_authorized
def add_item(admin_id):
    # Recupera i dati dal corpo della richiesta
    image_path = request.json.get("image_path")
    name = request.json.get("name")
    rarity = request.json.get("rarity")

    # Verifica che tutti i campi obbligatori siano presenti
    if not image_path or not name or not rarity:
        return jsonify({"message": "Missing mandatory fields"}), 400

    # Verifica la rarità dell'oggetto
    rarity_check = _check_rarity(rarity)
    if rarity_check:
        return rarity_check  # Ritorna la risposta di errore dal controllo di rarità

    # Crea il nuovo oggetto
    item = Item(image_path=image_path, name=name, rarity=rarity)

    try:
        db.session.add(item)
        db.session.commit()
        return jsonify(item.serialize()), 201
    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error while adding item: {str(e)}")
        return jsonify({"message": "An error occurred while adding the item"}), 400


@admin_api.route("/admin/<int:admin_id>/item/<int:item_id>", methods=["DELETE"])
@admin_token_authorized
def delete_item(admin_id, item_id):
    item = Item.query.get(item_id)
    if item:
        user_items = UserItem.query.filter_by(item_id=item_id).all()  # Corretto filtro per UserItem
        if user_items:
            return jsonify({
                "message": "It is not possible to delete an item if it is present in a user's collection"
            }), 400

        try:
            db.session.delete(item)
            db.session.commit()
            return jsonify({}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error while deleting item: {str(e)}")
            return jsonify({"message": "An error occurred while deleting the item"}), 400
    else:
        return jsonify({"message": "Item not found"}), 404

