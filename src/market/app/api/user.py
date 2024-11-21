import pytz
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
import logging

from helpers.token import token_authorized
from helpers.currency import CurrencyHelper
from helpers.collection import CollectionHelper
from models.models import Market, db

user_api = Blueprint('user_api', __name__)


@user_api.route("/user/<int:user_id>/market_list", methods=["GET"])
@token_authorized
def get_market_list(user_id):
    markets = Market.query.filter(
        Market.status == 'open'
    ).all()

    return jsonify([market.serialize() for market in markets]), 200


@user_api.route("/user/<int:user_id>/transactions_history", methods=["GET"])
@token_authorized
def get_transactions_history(user_id):
    transactions = Market.query.filter(
        (Market.seller_user_id == user_id) | (Market.buyer_user_id == user_id)
    ).all()

    return jsonify([transaction.serialize() for transaction in transactions]), 200


@user_api.route("/user/<int:user_id>/market/<int:market_id>/bid", methods=["PUT"])
@token_authorized
def place_bid(user_id, market_id):
    date_now = datetime.utcnow()
    bid_amount = request.json.get("bid_amount")

    if not bid_amount:
        return jsonify({"message": "bid is mandatory"}), 400

    auction = Market.query.filter(Market.market_id == market_id).first()
    if not auction:
        return jsonify({"message": "Auction not found"}), 404

    if date_now > auction.end_date:
        return jsonify({"message": "Auction expired"}), 400

    # Verifica che l'utente non stia facendo un'offerta sulla propria asta
    if auction.seller_user_id == user_id:
        return jsonify({"message": "You cannot bid on your own auction"}), 403

    # Verifica che l'offerta sia maggiore di quella attuale
    if bid_amount <= auction.bid:
        return jsonify({"message": "Bid must be higher than the current bid"}), 400
    try:
        CurrencyHelper().sub_amount(user_id, bid_amount)
        old_buyer_user_id = auction.buyer_user_id
        old_bid = auction.bid
        # Aggiorna l'asta con la nuova offerta
        auction.bid = bid_amount
        auction.buyer_user_id = user_id  # Imposta l'acquirente
        db.session.commit()
        if old_buyer_user_id:
            CurrencyHelper().add_amount(old_buyer_user_id, old_bid)
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error while place bid: {str(e)}")
        return (
            jsonify({"message": "An error occurred while processing your request."}),
            400,
        )

    return jsonify(auction.serialize()), 200


@user_api.route("/user/<int:user_id>/instance/<int:instance_id>/auction", methods=["PUT"])
@token_authorized
def set_auction(user_id, instance_id):
    utc_tz = pytz.utc
    date_now = datetime.utcnow().replace(tzinfo=utc_tz)
    end_date = request.json.get("end_date")
    start_bid = request.json.get("start_bid")

    if not end_date or not start_bid:
        return jsonify({"message": "end_date and start_bid are mandatory"}), 400

    if start_bid <= 0:
        return jsonify({"message": "start_bid must be a positive number"}), 400

    auction = Market.query.filter((Market.status == 'open') & (Market.istance_id == instance_id)).first()
    if auction:
        return jsonify({"message": "Auction already open"}), 400

    try:
        end_date = datetime.strptime(end_date, current_app.config["date_format"])
        local_tz = pytz.timezone('Europe/Rome')
        end_date = local_tz.localize(end_date)
        end_date_utc = end_date.astimezone(pytz.utc)
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

    response = CollectionHelper().get_instance(user_id, instance_id)   
    if response.status_code != 200:
        return jsonify({"message": "Unauthorized or invalid instance"}), 403

    new_auction = Market(
        istance_id=instance_id,
        seller_user_id=user_id,
        start_date=date_now,
        end_date=end_date_utc,
        status="open",
        bid=start_bid,
    )
    db.session.add(new_auction)
    db.session.commit()

    return jsonify(new_auction.serialize()), 201
