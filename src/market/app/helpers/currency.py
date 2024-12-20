import logging

from errors.errors import HTTPError
from utils_helpers.http_client import HttpClient
from flask import current_app


class CurrencyHelper:

    def __init__(self):
        self.base_url = current_app.config["currency"]

    def mock_currency_request(self, user_id, action, amount):
        if action == "add":
            return type(
                "MockResponse",
                (object,),
                {"status_code": 200, "json": lambda: {"message": "Mock add success"}},
            )()
        elif action == "sub":
            return type(
                "MockResponse",
                (object,),
                {"status_code": 200, "json": lambda: {"message": "Mock sub success"}},
            )()

    def add_amount(self, user_id, amount):
        if current_app.config["ENV"] == "testing":
            return self.mock_currency_request(user_id, "add", amount)
        else:
            response = HttpClient.post(
                f"{self.base_url}/user/{user_id}/add_amount",
                json={"amount": str(amount)},
            )
            if response.status_code != 200:
                HTTPError.raise_error_from_response(response)

            return response

    def sub_amount(self, user_id, amount):
        if current_app.config["ENV"] == "testing":
            return self.mock_currency_request(user_id, "sub", amount)
        else:
            response = HttpClient.post(
                f"{self.base_url}/user/{user_id}/sub_amount",
                json={"amount": str(amount)},
            )
            if response.status_code != 200:
                HTTPError.raise_error_from_response(response)

            return response
