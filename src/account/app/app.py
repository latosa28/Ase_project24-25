from flask import Flask, jsonify, request

app = Flask(__name__)


# Avvio dell'app Flask
if __name__ == '__main__':
    app.config['DEBUG'] = True  # Abilita il debug per ottenere errori più dettagliati
    app.run(host='0.0.0.0', port=5003)

