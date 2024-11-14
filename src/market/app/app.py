import logging
import os
from datetime import datetime

import requests
from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow

from models import db, Market

logging.basicConfig(level=logging.DEBUG)


DATE_FORMAT = "%d/%m/%Y %H:%M"


def load_config():
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


app = Flask(__name__)
load_config()
db.init_app(app)  # Qui inizializziamo il db con l'app
ma = Marshmallow(app)

COLLECTION_URL = "http://collection:5002"
CURRENCY_URL = "http://currency:5005"


@app.route("/user/<int:user_id>/market_list", methods=["GET"])
def get_market_list(user_id):
    markets = Market.query.filter(
        (Market.seller_user_id == user_id)
        | (Market.buyer_user_id == user_id)
        | (Market.end_date > datetime.utcnow())
    ).all()

    return jsonify([market.serialize() for market in markets]), 200


@app.route("/user/<int:user_id>/transactions_history", methods=["GET"])
def get_transactions_history(user_id):
    transactions = Market.query.filter(
        (Market.seller_user_id == user_id) | (Market.buyer_user_id == user_id)
    ).all()

    return jsonify([transaction.serialize() for transaction in transactions]), 200


@app.route("/user/<int:user_id>/market/<int:market_id>/bid", methods=["PUT"])
def place_bid(user_id, market_id):

    bid_amount = request.json.get("bid_amount")

    if not bid_amount:
        return jsonify({"message": "bid is mandatory"}), 400

    # Recupera l'asta specificata
    auction = Market.query.get(market_id)
    if not auction:
        return jsonify({"message": "Auction not found"}), 404

    # Verifica che l'utente non stia facendo un'offerta sulla propria asta
    if auction.seller_user_id == user_id:
        return jsonify({"message": "You cannot bid on your own auction"}), 403

    # Verifica che l'offerta sia maggiore di quella attuale
    if bid_amount <= auction.bid:
        return jsonify({"message": "Bid must be higher than the current bid"}), 400
    try:
        response = requests.post(
            CURRENCY_URL + f"/user/{user_id}/sub_amount",
            json={"amount": str(bid_amount)},
        )
        if response.status_code != 200:
            raise Exception("Buyer dont'have enough amount")
        old_buyer_user_id = auction.buyer_user_id
        old_bid = auction.bid
        # Aggiorna l'asta con la nuova offerta
        auction.bid = bid_amount
        auction.buyer_user_id = user_id  # Imposta l'acquirente
        db.session.commit()
        if old_buyer_user_id:
            response = requests.post(
                CURRENCY_URL + f"/user/{old_buyer_user_id}/add_amount",
                json={"amount": str(old_bid)},
            )
            if response.status_code != 200:
                raise Exception("Amount was not returned to the old buyer")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while place bid: {str(e)}")
        return (
            jsonify({"message": "An error occurred while processing your request."}),
            400,
        )

    return jsonify(auction.serialize()), 200


@app.route("/user/<int:user_id>/instance/<int:instance_id>/auction", methods=["PUT"])
def set_auction(user_id, instance_id):
    date_now = datetime.utcnow()
    end_date = request.json.get("end_date")
    start_bid = request.json.get("start_bid")

    if not end_date or not start_bid:
        return jsonify({"message": "end_date and start_bid are mandatory"}), 400

    try:
        end_date = datetime.strptime(end_date, DATE_FORMAT)
    except ValueError as e:
        return (
            jsonify(
                {
                    "message": "end_date format is wrong, correct format is dd/mm/YYYY HH:MM "
                }
            ),
            400,
        )

    if not end_date > date_now:
        return jsonify({"message": "end_date must be in the future"}), 400

    # Verifica se l'utente ha il diritto di creare un'asta per questa istanza
    response = requests.get(COLLECTION_URL + f"/user/{user_id}/instance/{instance_id}")
    if response.status_code != 200:
        return jsonify({"message": "Unauthorized or invalid instance"}), 403

    new_auction = Market(
        istance_id=instance_id,
        seller_user_id=user_id,
        start_date=date_now,
        end_date=end_date,
        bid=start_bid,
    )
    db.session.add(new_auction)
    db.session.commit()

    return jsonify(new_auction.serialize()), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)
