import pytz
from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
import logging

from errors.errors import HTTPBadRequestError, HTTPForbiddenError, HTTPNotFoundError, HTTPError
from utils_helpers.token import token_authorized
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
        raise HTTPBadRequestError("bid is mandatory")

    auction = Market.query.filter(Market.market_id == market_id).first()
    if not auction:
        raise HTTPNotFoundError("Auction not found")

    if date_now > auction.end_date:
        raise HTTPBadRequestError("Auction expired")

    # Verifica che l'utente non stia facendo un'offerta sulla propria asta
    if auction.seller_user_id == user_id:
        raise HTTPForbiddenError("You cannot bid on your own auction")

    # Verifica che l'offerta sia maggiore di quella attuale
    if bid_amount <= auction.bid:
        raise HTTPBadRequestError("Bid must be higher than the current bid")

    CurrencyHelper().sub_amount(user_id, bid_amount)
    try:
        old_buyer_user_id = auction.buyer_user_id
        old_bid = auction.bid
        auction.bid = bid_amount
        auction.buyer_user_id = user_id  # Imposta l'acquirente
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        CurrencyHelper().add_amount(user_id, bid_amount)
        raise e

    if old_buyer_user_id:
        CurrencyHelper().add_amount(old_buyer_user_id, old_bid)

    return jsonify(auction.serialize()), 200


@user_api.route("/user/<int:user_id>/instance/<int:instance_id>/auction", methods=["PUT"])
@token_authorized
def set_auction(user_id, instance_id):
    utc_tz = pytz.utc
    date_now = datetime.utcnow().replace(tzinfo=utc_tz)
    end_date = request.json.get("end_date")
    start_bid = request.json.get("start_bid")

    if not end_date or not start_bid:
        raise HTTPBadRequestError("end_date and start_bid are mandatory")

    if start_bid <= 0:
        raise HTTPBadRequestError("start_bid must be a positive number")

    auction = Market.query.filter((Market.status == 'open') & (Market.istance_id == instance_id)).first()
    if auction:
        raise HTTPBadRequestError("Auction already open")

    try:
        end_date = datetime.strptime(end_date, current_app.config["date_format"])
        local_tz = pytz.timezone('Europe/Rome')
        end_date = local_tz.localize(end_date)
        end_date_utc = end_date.astimezone(pytz.utc)
    except ValueError as e:
        raise HTTPBadRequestError("end_date format is wrong, correct format is dd/mm/YYYY HH:MM ")

    if not end_date > date_now:
        raise HTTPBadRequestError("end_date must be in the future")

    response = CollectionHelper().get_instance(user_id, instance_id)   
    if response.status_code != 200:
        raise HTTPForbiddenError("Unauthorized or invalid instance")
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
