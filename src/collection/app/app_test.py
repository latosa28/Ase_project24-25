import collection  # Importa il microservizio collection
from flask import Flask
from flask.testing import FlaskClient

# Crea un'app di test Flask basata sull'app principale
test_app = collection.app
test_client = test_app.test_client()


# Funzione mock per simulare le risposte del servizio `currency`
def mock_currency_request(user_id, amount):
    if user_id == 1:  # Esempio di comportamento mockato
        return type('MockResponse', (object,), {"status_code": 200, "json": lambda: {"message": "Mock success"}})()
    else:
        return type('MockResponse', (object,), {"status_code": 400, "json": lambda: {"error": "Mock failure"}})()


# Imposta la funzione mock nel file collection
collection.currency_request_function = mock_currency_request


