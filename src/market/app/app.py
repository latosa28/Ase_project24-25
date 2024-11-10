from flask import Flask, jsonify, request

app = Flask(__name__)

# Dizionario per memorizzare gli oggetti nel mercato
market_items = {
    "pikachu_toy": {"name": "Pikachu Toy", "price": 500},
    "charmander_toy": {"name": "Charmander Toy", "price": 300},
    "squirtle_toy": {"name": "Squirtle Toy", "price": 200}
}

# Dizionario per memorizzare gli oggetti posseduti dagli utenti
user_items = {
    "user1": [],
    "user2": ["pikachu_toy"],
    "user3": ["charmander_toy", "squirtle_toy"]
}

# Dizionario per memorizzare il saldo della valuta degli utenti
users_balance = {
    "user1": 1000,
    "user2": 500,
    "user3": 2500
}

# Endpoint per ottenere la lista degli oggetti nel mercato
@app.route('/market/items', methods=['GET'])
def get_market_items():
    return jsonify(market_items), 200

# Endpoint per acquistare un oggetto dal mercato
@app.route('/market/buy', methods=['POST'])
def buy_item():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")

    if user_id not in users_balance:
        return jsonify({"error": "User not found"}), 404

    if item_id not in market_items:
        return jsonify({"error": "Item not found in market"}), 404

    item = market_items[item_id]
    item_price = item["price"]

    if users_balance[user_id] < item_price:
        return jsonify({"error": "Insufficient balance"}), 400

    # Acquista l'oggetto
    users_balance[user_id] -= item_price
    user_items[user_id].append(item_id)

    return jsonify({"message": f"Purchased {item['name']}", "new_balance": users_balance[user_id]}), 200

# Endpoint per vendere un oggetto nel mercato
@app.route('/market/sell', methods=['POST'])
def sell_item():
    data = request.json
    user_id = data.get("user_id")
    item_id = data.get("item_id")

    if user_id not in user_items or item_id not in user_items[user_id]:
        return jsonify({"error": "Item not found in user inventory"}), 404

    if item_id not in market_items:
        return jsonify({"error": "Item not found in market"}), 404

    item = market_items[item_id]
    item_price = item["price"]

    # Vende l'oggetto
    user_items[user_id].remove(item_id)
    users_balance[user_id] += item_price

    return jsonify({"message": f"Sold {item['name']}", "new_balance": users_balance[user_id]}), 200

# Avvio dell'app Flask
if __name__ == '__main__':
    app.config['DEBUG'] = True  # Abilita il debug per ottenere errori più dettagliati
    app.run(host='0.0.0.0', port=5004)
