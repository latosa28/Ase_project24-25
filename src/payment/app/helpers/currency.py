from utils_helpers.http_client import HttpClient
from flask import current_app


class CurrencyHelper:

    def __init__(self):
        self.base_url = current_app.config["currency"]

    def mock_currency_request(self, user_id, amount):
        if user_id == 1:
            return type('MockResponse', (object,), {"status_code": 200, "json": lambda: {"message": "Mock add success"}})()
        else:
            return type('MockResponse', (object,), {"status_code": 400, "json": lambda: {"error": "Mock failure"}})()

    def add_amount(self, user_id, amount):
        if current_app.config['ENV'] == 'testing':
            return self.mock_currency_request(user_id, amount)
        else:
            response = HttpClient.post(
                f"{self.base_url}/user/{user_id}/add_amount",
                json={"amount": str(amount)},
            )
            return response
