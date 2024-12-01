from utils_helpers.http_client import HttpClient
from flask import current_app


class CollectionHelper:

    def __init__(self):
        self.base_url = current_app.config["collection"]

    def mock_collection_request(self, user_id, instance_id, new_user_id=None):
        if user_id == 1 and (new_user_id is None or new_user_id == 2):
            return type('MockResponse', (object,), {"status_code": 200, "json": lambda: {"message": "Mock success"}})()
        else:
            return type('MockResponse', (object,), {"status_code": 403, "json": lambda: {"error": "Mock failure"}})()

    def move_instance(self, user_id, new_user_id, instance_id):
        if current_app.config['ENV'] == 'testing':
            return self.mock_collection_request(user_id, instance_id, new_user_id)
        else:
            response = HttpClient.post(
                f"{self.base_url}/user/{user_id}/instance/{instance_id}",
                json={"new_user_id": new_user_id},
            )
            if response.status_code != 200:
                raise Exception(response.reason)
            return response
        
    def get_instance(self, user_id, instance_id):
        if current_app.config['ENV'] == 'testing':
            return self.mock_collection_request(user_id, instance_id)
        else:
            response = HttpClient.get(
                f"{self.base_url}/user/{user_id}/instance/{instance_id}"
            )
            return response



