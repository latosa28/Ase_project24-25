import logging
from flask import Blueprint, jsonify

from models.models import Market, db

admin_api = Blueprint('admin_api', __name__)


@admin_api.route("/admin/<int:admin_id>/market_list", methods=["GET"])
def get_market_list(admin_id):
    try:
        # Recupera tutti i mercati con status "open"
        markets = Market.query.filter(Market.status == 'open').all()

        # Serializza i dati e restituisce la risposta
        return jsonify([market.serialize() for market in markets]), 200
    except Exception as e:
        logging.error(f"Error retrieving market list: {str(e)}")
        return jsonify({"message": "An error occurred while retrieving the market list"}), 500



@admin_api.route("/admin/<int:admin_id>/user/<int:user_id>/transactions_history", methods=["GET"])
def get_user_transactions_history(admin_id, user_id):
    try:
        # Recupera le transazioni in cui l'utente è coinvolto come compratore o venditore
        transactions = Market.query.filter(
            (Market.seller_user_id == user_id) | (Market.buyer_user_id == user_id)
        ).all()

        # Serializza e restituisce le transazioni
        return jsonify([transaction.serialize() for transaction in transactions]), 200
    except Exception as e:
        logging.error(f"Error retrieving transaction history for user {user_id}: {str(e)}")
        return jsonify({"message": "An error occurred while retrieving the transaction history"}), 500



@admin_api.route("/admin/<int:admin_id>/transactions_history", methods=["GET"])
def get_transactions_history(admin_id):
    try:
        # Recupera tutte le transazioni dal database
        transactions = Market.query.all()

        # Serializza e restituisce le transazioni
        return jsonify([transaction.serialize() for transaction in transactions]), 200
    except Exception as e:
        logging.error(f"Error retrieving transaction history: {str(e)}")
        return jsonify({"message": "An error occurred while retrieving transaction history"}), 500



@admin_api.route("/admin/<int:admin_id>/market/<int:market_id>", methods=["GET"])
def get_auction(admin_id, market_id):
    try:
        # Recupera l'asta dal database
        auction = Market.query.filter(Market.market_id == market_id).first()
        
        if not auction:
            return jsonify({"message": "Auction not found"}), 404

        # Serializza e restituisce l'asta
        return jsonify(auction.serialize()), 200
    except Exception as e:
        logging.error(f"Error retrieving auction: {str(e)}")
        return jsonify({"message": "An error occurred while retrieving the auction"}), 500



@admin_api.route("/admin/<int:admin_id>/market/<int:market_id>", methods=["POST"])
def cancel_auction(admin_id, market_id):
    try:
        # Verifica se l'asta esiste
        auction = Market.query.filter(Market.market_id == market_id).first()

        if not auction:
            return jsonify({"message": "Auction not found"}), 404

        if auction.status == 'closed':
            return jsonify({"message": "Auction is already closed"}), 400

        # Modifica lo stato dell'asta
        auction.status = 'closed'
        db.session.commit()

        return jsonify({"message": "Auction successfully closed"}), 200
    except Exception as e:
        logging.error(f"Error while closing auction: {str(e)}")
        db.session.rollback()
        return (
            jsonify({"message": "An error occurred while processing your request."}),
            500,
        )





