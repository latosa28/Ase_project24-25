import requests
from flask import current_app


class CurrencyHelper:

    def __init__(self):
        self.base_url = current_app.config["currency"]

    def add_amount(self, user_id, amount):
        response = requests.post(
            f"{self.base_url}/user/{user_id}/add_amount",
            json={"amount": str(amount)},
        )
        if response.status_code != 200:
            raise Exception(response.reason)
