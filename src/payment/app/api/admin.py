from flask import Blueprint, jsonify, request

from models.models import Transactions

admin_api = Blueprint("admin_api", __name__)


@admin_api.route("/admin/<int:admin_id>/user/<int:user_id>/currency_history", methods=["GET"])
def get_user_transactions(admin_id, user_id):
    user_transactions = Transactions.query.filter_by(user_id=user_id).all()
    return jsonify([transaction.serialize() for transaction in user_transactions]), 200
