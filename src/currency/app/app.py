from flask import Flask, jsonify, request

app = Flask(__name__)

# Dizionario per memorizzare gli importi per ciascun utente
# Popolato con esempi di utenti e saldi iniziali
users_balance = {
    "user1": 1000,  # Utente con saldo iniziale di 1000
    "user2": 500,   # Utente con saldo iniziale di 500
    "user3": 2500,  # Utente con saldo iniziale di 2500
    "user4": 0      # Utente con saldo iniziale di 0
}


# Endpoint per ottenere l'importo (amount) della valuta di un utente
@app.route('/user/<user_id>/amount', methods=['GET'])
def get_amount(user_id):
    # Controlla se l'utente ha un saldo
    if user_id in users_balance:
        return jsonify({"user_id": user_id, "amount": users_balance[user_id]}), 200
    return jsonify({"error": "User not found"}), 404


# Endpoint per aggiungere una quantità all'importo della valuta di un utente
@app.route('/user/<user_id>/add_amount', methods=['POST'])
def add_amount(user_id):
    # Ottieni l'importo da aggiungere dal corpo della richiesta
    data = request.json
    amount_to_add = data.get("amount")

    if amount_to_add is None:
        return jsonify({"error": "Amount is required"}), 400

    if user_id in users_balance:
        users_balance[user_id] += amount_to_add
    else:
        users_balance[user_id] = amount_to_add

    return jsonify({"message": f"Added {amount_to_add} to {user_id}'s balance", "new_balance": users_balance[user_id]}), 200


# Endpoint per sottrarre una quantità dall'importo della valuta di un utente
@app.route('/user/<user_id>/sub_amount', methods=['POST'])
def sub_amount(user_id):
    # Ottieni l'importo da sottrarre dal corpo della richiesta
    data = request.json
    amount_to_sub = data.get("amount")

    if amount_to_sub is None:
        return jsonify({"error": "Amount is required"}), 400

    if user_id in users_balance:
        if users_balance[user_id] >= amount_to_sub:
            users_balance[user_id] -= amount_to_sub
            return jsonify({"message": f"Subtracted {amount_to_sub} from {user_id}'s balance", "new_balance": users_balance[user_id]}), 200
        else:
            return jsonify({"error": "Insufficient balance"}), 400
    else:
        return jsonify({"error": "User not found"}), 404


# Avvio dell'app Flask
if __name__ == '__main__':
    app.config['DEBUG'] = True  # Abilita il debug per ottenere errori più dettagliati
    app.run(host='0.0.0.0', port=5005)
