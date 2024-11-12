from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configura la connessione al database (assicurati di impostare le variabili d'ambiente)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inizializza SQLAlchemy
db = SQLAlchemy(app)

# Modello per rappresentare il saldo di ciascun utente nel database
class currency(db.Model):
    __tablename__ = 'currency'
    user_id = db.Column(db.String(50), primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)

    def __init__(self, user_id, amount=0.0):
        self.user_id = user_id
        self.amount = amount

# Endpoint per ottenere il saldo di un utente
@app.route('/user/<user_id>/amount', methods=['GET'])
def get_amount(user_id):
    amount = currency.query.filter_by(user_id=user_id).first()
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

    # Cerca l'utente nel database
    amount = currency.query.filter_by(user_id=user_id).first()
    
    if amount is None:
        # Se l'utente non esiste, creiamo una nuova riga per lui
        amount =currency(user_id=user_id, amount=amount_to_add)
        db.session.add(amount)
    else:
        # Se l'utente esiste, aggiorniamo il saldo
        amount.amount += amount_to_add

    # Commit per salvare le modifiche
    db.session.commit()
    return jsonify({"message": f"Added {amount_to_add} to {user_id}'s balance", "new_balance": amount.amount}), 200


# Endpoint per sottrarre una quantità dal saldo di un utente
@app.route('/user/<user_id>/sub_amount', methods=['POST'])
def sub_amount(user_id):
    data = request.json
    try:
        amount_to_sub = float(data.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a valid number"}), 400

    # Cerca l'utente nel database
    amount = currency.query.filter_by(user_id=user_id).first()

    if amount is None:
        # Se l'utente non esiste, creiamo una nuova riga con saldo iniziale zero
        amount = currency(user_id=user_id, amount=0.0)
        db.session.add(amount)
        db.session.commit()
        return jsonify({"error": "User balance was zero; cannot subtract requested amount"}), 400

    # Controlla se l'utente ha saldo sufficiente per la sottrazione
    if amount.amount >= amount_to_sub:
        amount.amount -= amount_to_sub
        db.session.commit()
        return jsonify({"message": f"Subtracted {amount_to_sub} from {user_id}'s balance", "new_balance": amount.amount}), 200
    else:
        return jsonify({"error": "Insufficient balance"}), 400

# Avvio dell'app Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
