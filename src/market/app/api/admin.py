from flask import Blueprint, jsonify

from models.models import Market, db

admin_api = Blueprint('admin_api', __name__)


@admin_api.route("/admin/<int:admin_id>/market_list", methods=["GET"])
def get_market_list(admin_id):
    markets = Market.query.filter(
        Market.status == 'open'
    ).all()

    return jsonify([market.serialize() for market in markets]), 200


@admin_api.route("/admin/<int:admin_id>/user/<int:user_id>/transactions_history", methods=["GET"])
def get_user_transactions_history(admin_id, user_id):
    transactions = Market.query.filter(
        (Market.seller_user_id == user_id) | (Market.buyer_user_id == user_id)
    ).all()

    return jsonify([transaction.serialize() for transaction in transactions]), 200


@admin_api.route("/admin/<int:admin_id>/transactions_history", methods=["GET"])
def get_transactions_history(admin_id):
    transactions = Market.query.all()
    return jsonify([transaction.serialize() for transaction in transactions]), 200


@admin_api.route("/admin/<int:admin_id>/market/<int:market_id>", methods=["GET"])
def get_auction(admin_id, market_id):
    auction = Market.query.filter(Market.market_id == market_id).first()
    return jsonify(auction.serialize()), 200


@admin_api.route("/admin/<int:admin_id>/market/<int:market_id>", methods=["POST"])
def cancel_auction(admin_id, market_id):
    auction = Market.query.filter(Market.market_id == market_id).first()
    try:
        auction.status = 'closed'
        db.session.commit()
    except Exception:
        db.session.rollback()
        return (
            jsonify({"message": "An error occurred while processing your request."}),
            400,
        )





