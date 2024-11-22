from flask import Flask, jsonify, request
import os

from utils.helpers.token import token_authorized
from utils.helpers.auth import AuthHelper
from models.models import db, Currency

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_env = os.getenv('FLASK_ENV', 'production')
app.config['ENV'] = flask_env
db.init_app(app)
public_key = AuthHelper.get_jwt_public_key(app.config['ENV'])
app.config["jwt_public_key"] = public_key


def create_currency_row(user_id, amount):
    amount = Currency(user_id=user_id, amount=amount)
    db.session.add(amount)
    db.session.commit()


# Endpoint per ottenere il saldo di un utente
@app.route('/user/<int:user_id>/amount', methods=['GET'])
@token_authorized
def get_amount(user_id):
    amount = Currency.query.filter_by(user_id=user_id).first()
    if amount:
        return jsonify({"user_id": user_id, "amount": amount.amount}), 200
    return jsonify({"error": "User not found"}), 404


# Endpoint per aggiungere una quantità al saldo di un utente
@app.route('/user/<user_id>/add_amount', methods=['POST'])
def add_amount(user_id):
    data = request.json
    try:
        amount_to_add = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a valid number"}), 400

    amount = Currency.query.filter_by(user_id=user_id).first()
    
    if amount is None:
        create_currency_row(user_id, amount_to_add)
    else:
        amount.amount += amount_to_add

    db.session.commit()
    return jsonify({}), 200


# Endpoint per sottrarre una quantità dal saldo di un utente
@app.route('/user/<user_id>/sub_amount', methods=['POST'])
def sub_amount(user_id):
    data = request.json
    try:
        amount_to_sub = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a valid number"}), 400

    amount = Currency.query.filter_by(user_id=user_id).first()

    if amount is None:
        create_currency_row(user_id, 0)
        return jsonify({"error": "User balance was zero - cannot subtract requested amount"}), 400

    if amount.amount >= amount_to_sub:
        amount.amount -= amount_to_sub
        db.session.commit()
        return jsonify({}), 200
    else:
        return jsonify({"error": "Insufficient balance"}), 400


# Avvio dell'app Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
