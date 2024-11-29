import logging
from flask import Blueprint, jsonify

from errors.errors import HTTPBadRequestError, HTTPNotFoundError
from utils_helpers.token import admin_token_authorized
from models.models import Market, db

admin_api = Blueprint('admin_api', __name__)


@admin_api.route("/admin/<int:admin_id>/market_list", methods=["GET"])
@admin_token_authorized
def get_market_list(admin_id):
    markets = Market.query.filter(Market.status == 'open').all()
    return jsonify([market.serialize() for market in markets]), 200


@admin_api.route("/admin/<int:admin_id>/user/<int:user_id>/transactions_history", methods=["GET"])
@admin_token_authorized
def get_user_transactions_history(admin_id, user_id):
    transactions = Market.query.filter(
        (Market.seller_user_id == user_id) | (Market.buyer_user_id == user_id)
    ).all()
    return jsonify([transaction.serialize() for transaction in transactions]), 200


@admin_api.route("/admin/<int:admin_id>/transactions_history", methods=["GET"])
@admin_token_authorized
def get_transactions_history(admin_id):
    transactions = Market.query.all()
    return jsonify([transaction.serialize() for transaction in transactions]), 200


@admin_api.route("/admin/<int:admin_id>/market/<int:market_id>", methods=["GET"])
def get_auction(admin_id, market_id):
    auction = Market.query.filter(Market.market_id == market_id).first()
        
    if not auction:
        raise HTTPNotFoundError("Auction not found")

    return jsonify(auction.serialize()), 200


@admin_api.route("/admin/<int:admin_id>/market/<int:market_id>", methods=["POST"])
@admin_token_authorized
def cancel_auction(admin_id, market_id):
    try:
        auction = Market.query.filter(Market.market_id == market_id).first()

        if not auction:
            raise HTTPNotFoundError("Auction not found")

        if auction.status == 'closed':
            raise HTTPBadRequestError("Auction is already closed")

        auction.status = 'closed'
        db.session.commit()
        return jsonify({"message": "Auction successfully closed"}), 200
    except Exception as e:
        logging.error(f"Error while closing auction: {str(e)}")
        db.session.rollback()
        raise HTTPBadRequestError("An error occurred while processing your request.")
        





