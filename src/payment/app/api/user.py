import json
from datetime import datetime

import pytz
from flask import Blueprint, jsonify, request, current_app

from helpers.currency import CurrencyHelper
from errors.errors import HTTPBadRequestError, HTTPInternalServerError
from utils_helpers.AES import encrypt_data
from utils_helpers.token import token_required, token_authorized

from models.models import db, Transactions
from utils_helpers.validation import get_body_field

user_api = Blueprint("user_api", __name__)


def convert_to_special_currency(amount):
    conversion_rate = current_app.config["currency_conversion_rate"]
    return amount * conversion_rate


def simulate_payment(card_number, card_expiry, card_cvc, amount):
    return True


# Route to buy currency
@user_api.route("/user/<int:user_id>/payment", methods=["POST"])
@token_authorized
def payment(user_id):
    data = request.get_json()

    if (
        "card_number" not in data
        or "card_expiry" not in data
        or "card_cvc" not in data
        or "amount" not in data
    ):
        raise HTTPBadRequestError("Missing required fields")

    card_number = data["card_number"]
    card_expiry = data["card_expiry"]
    card_cvc = data["card_cvc"]
    amount = get_body_field("amount", expected_type=float)

    success = simulate_payment(card_number, card_expiry, card_cvc, amount)
    currency_amount = convert_to_special_currency(amount)

    transaction_status = "success" if success else "failed"

    transaction_data = json.dumps(
        {
            "amount": amount,
            "currency_amount": currency_amount,
            "status": transaction_status,
        }
    )

    transaction = Transactions(
        user_id=user_id,
        transaction_data=encrypt_data(transaction_data),
        creation_time=datetime.utcnow().replace(tzinfo=pytz.utc),
    )

    db.session.add(transaction)
    db.session.commit()

    if success:
        response = CurrencyHelper().add_amount(user_id, currency_amount)
        if response.status_code == 200:
            return (
                jsonify(
                    {
                        "message": "Payment successful",
                        "amount_paid": amount,
                        "currency_received": currency_amount,
                    }
                ),
                200,
            )
    else:
        raise HTTPInternalServerError("Payment failed")
