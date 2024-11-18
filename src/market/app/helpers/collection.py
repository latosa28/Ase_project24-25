import requests
from flask import current_app


class CollectionHelper:

    def __init__(self):
        self.base_url = current_app.config["collection"]

    def move_instance(self, user_id, new_user_id, instance_id):
        response = requests.post(
            f"{self.base_url}/user/{user_id}/instance/{instance_id}",
            json={"new_user_id": new_user_id},
        )
        if response.status_code != 200:
            raise Exception(response.reason)


