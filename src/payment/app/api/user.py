from datetime import datetime

import pytz
from flask import Blueprint, jsonify, request, current_app

from helpers.currency import CurrencyHelper
from errors.errors import HTTPBadRequestError, HTTPInternalServerError
from utils_helpers.token import token_required

from models.models import db, Transactions

user_api = Blueprint('user_api', __name__)


def convert_to_special_currency(amount):
    conversion_rate = current_app.config["currency_conversion_rate"]
    return amount * conversion_rate


def simulate_payment(card_number, card_expiry, card_cvc, amount):
    return True


# Route to buy currency
@user_api.route('/user/<int:user_id>/payment', methods=['POST'])
@token_required
def payment(user_id):
    data = request.get_json()

    if 'card_number' not in data or 'card_expiry' not in data or 'card_cvc' not in data or 'amount' not in data:
        raise HTTPBadRequestError("Missing required fields")

    card_number = data['card_number']
    card_expiry = data['card_expiry']
    card_cvc = data['card_cvc']
    amount = data['amount']

    success = simulate_payment(card_number, card_expiry, card_cvc, amount)
    currency_amount = convert_to_special_currency(amount)

    transaction_status = 'success' if success else 'failed'
    transaction = Transactions(
        user_id=user_id,
        card_number=card_number,
        card_expiry=card_expiry,
        card_cvc=card_cvc,
        amount=amount,
        currency_amount=currency_amount,
        status=transaction_status,
        creation_time=datetime.utcnow().replace(tzinfo=pytz.utc)
    )
    db.session.add(transaction)
    db.session.commit()

    if success:
        response = CurrencyHelper().add_amount(user_id, currency_amount)
        return jsonify({
            'message': 'Payment successful',
            'amount_paid': amount,
            'currency_received': currency_amount if response.status_code == 200 else 0,
        }), 200
    else:
        raise HTTPInternalServerError("Payment failed")
