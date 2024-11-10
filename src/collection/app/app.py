from flask import Flask, jsonify, request

app = Flask(__name__)

# Dizionario per memorizzare i dati del gacha
# Ogni utente ha una propria collezione di Pokémon
users = {
    "user1": {
        "pikachu": {"id": "pikachu", "name": "Pikachu", "type": "Electric"},
        "charmander": {"id": "charmander", "name": "Charmander", "type": "Fire"}
    },
    "user2": {
        "squirtle": {"id": "squirtle", "name": "Squirtle", "type": "Water"}
    }
}

# Endpoint per ottenere la collezione gacha del sistema
@app.route('/collection', methods=['GET'])
def get_system_collection():
    # Restituisce la collezione globale di Pokémon (che potrebbe essere una lista di tutti i Pokémon possibili)
    system_collection = {
        "pikachu": {"id": "pikachu", "name": "Pikachu", "type": "Electric"},
        "charmander": {"id": "charmander", "name": "Charmander", "type": "Fire"},
        "squirtle": {"id": "squirtle", "name": "Squirtle", "type": "Water"}
    }
    return jsonify(system_collection), 200

# Endpoint per ottenere le informazioni di un singolo item della collezione di sistema
@app.route('/item/<item_id>', methods=['GET'])
def get_item_info(item_id):
    system_collection = {
        "pikachu": {"id": "pikachu", "name": "Pikachu", "type": "Electric"},
        "charmander": {"id": "charmander", "name": "Charmander", "type": "Fire"},
        "squirtle": {"id": "squirtle", "name": "Squirtle", "type": "Water"}
    }
    
    item = system_collection.get(item_id)
    if item:
        return jsonify(item), 200
    return jsonify({"error": "Item not found"}), 404

# Endpoint per ottenere la collezione di un utente specifico
@app.route('/user/<user_id>/collection', methods=['GET'])
def get_user_collection(user_id):
    user_collection = users.get(user_id)
    if user_collection:
        return jsonify(user_collection), 200
    return jsonify({"error": "User collection not found"}), 404

# Endpoint per ottenere le informazioni di un'istanza specifica della collezione di un utente
@app.route('/user/<user_id>/instance/<instance_id>', methods=['GET'])
def get_user_instance(user_id, instance_id):
    user_collection = users.get(user_id)
    if user_collection and instance_id in user_collection:
        return jsonify(user_collection[instance_id]), 200
    return jsonify({"error": "Instance not found"}), 404

# Endpoint per eseguire il "roll" (aggiornamento o aggiunta) di un item nella collezione dell'utente
@app.route('/user/<user_id>/roll', methods=['PUT'])
def roll_gacha(user_id):
    new_item = request.json
    item_id = new_item.get("id")
    
    if not item_id:
        return jsonify({"error": "Item ID is required"}), 400
    
    # Se l'utente non esiste ancora, creiamo la sua collezione
    if user_id not in users:
        users[user_id] = {}
    
    # Aggiunge o aggiorna l'item nella collezione dell'utente
    users[user_id][item_id] = new_item
    return jsonify({"message": "Item rolled successfully", "item": new_item}), 200

# Avvio dell'app Flask
if __name__ == '__main__':
    app.config['DEBUG'] = True  # Abilita il debug per ottenere errori più dettagliati
    app.run(host='0.0.0.0', port=5002)
