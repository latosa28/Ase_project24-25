from utils_helpers.http_client import HttpClient
from flask import current_app

CURRENCY_URL = "https://currency:5005"


class CurrencyHelper:

    def mock_currency_request(self, user_id, amount):
        if user_id == 1:
            return type('MockResponse', (object,), {"status_code": 200, "json": lambda: {"message": "Mock success"}})()
        else:
            return type('MockResponse', (object,), {"status_code": 400, "json": lambda: {"error": "Mock failure"}})()

    def sub_amount(self, user_id, amount):
        if current_app.config['ENV'] == 'testing':
            return self.mock_currency_request(user_id, amount)
        else:
            return HttpClient.post(CURRENCY_URL + f'/user/{user_id}/sub_amount', json={"amount": amount})