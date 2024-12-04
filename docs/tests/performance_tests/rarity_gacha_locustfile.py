from locust import HttpUser, task, between
import random
import json
import time 

class RarityGachaTestUser(HttpUser):
    wait_time = between(0.1, 0.2)
    user_counter = 0

    def on_start(self):
        """Initialize the user, log in and prepare necessary data."""
        self.__class__.user_counter += 1
        self.user_id = self.__class__.user_counter
        self.username = f"user_{self.user_id}"
        self.email = f"user_{self.user_id}@example.com"
        self.password = "password123"

        # Sleep to avoid server overload
        time.sleep(self.user_id * 0.5)

        # Create user, login and get a token
        if not self.create_user():
            return

        if not self.login():
            return

        if not self.add_funds(10000): 
            return

        self.rarity_counts = {
            "superultrarare": 0,
            "ultrarare": 0,
            "superrare": 0,
            "rare": 0,
            "common": 0
        }
        self.total_rolls = 0

    def create_user(self):
        """Create a new user with unique data."""
        response = self.client.post("/user", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        }, verify=False)  # Disable SSL verification

        if response.status_code == 201:
            print(f"User {self.username} created successfully.")
            return True
        else:
            print(f"Error creating user {self.username}: {response.text}")
            return False

    def login(self):
        """Log the user in to obtain a token."""
        response = self.client.post("/user/auth", json={
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }, verify=False)  # Disable SSL verification

        if response.status_code == 200:
            self.headers = {
                "Authorization": f"Bearer {response.json()['access_token']}"
            }
            print(f"User {self.username} logged in successfully.")
            return True
        else:
            print(f"Login failed for user {self.username}: {response.text}")
            return False

    def add_funds(self, amount):
        """Add funds to the user's account."""
        response = self.client.post(f"/user/{self.user_id}/payment", json={
            "card_number": "4111111111111111",
            "card_expiry": "12/26",
            "card_cvc": "123",
            "amount": amount
        }, verify=False)  # Disable SSL verification

        if response.status_code == 200:
            print(f"Added {amount} currency to user {self.username}.")
            return True
        else:
            print(f"Error adding funds for user {self.username}: {response.text}")
            return False

    @task(3)
    def roll_gacha(self):
        """Simulate a gacha roll."""
        response = self.client.put(f"/user/{self.user_id}/roll", headers=self.headers, verify=False)  # Disable SSL verification
        if response.status_code == 201:
            self.total_rolls += 1
            try:
                rarity = response.json().get("rarity")
                if rarity in self.rarity_counts:
                    self.rarity_counts[rarity] += 1
            except json.JSONDecodeError:
                print(f"Error decoding JSON response for user {self.user_id}.")
        else:
            print(f"Roll failed for user {self.user_id}. Status: {response.status_code}")

    def on_stop(self):
        """Summarize results at the end of the test."""
        print(f"--- Final statistics for User {self.user_id} ---")
        print(f"Total rolls: {self.total_rolls}")
        for rarity, count in self.rarity_counts.items():
            percentage = (count / self.total_rolls) * 100 if self.total_rolls > 0 else 0
            print(f"{rarity}: {count} ({percentage:.2f}%)")
        
        expected_distribution = {
            "superultrarare": 0.05,
            "ultrarare": 0.5,
            "superrare": 5.0,
            "rare": 40.0,
            "common": 54.45
        }

        for rarity, expected_percentage in expected_distribution.items():
            actual_percentage = (self.rarity_counts.get(rarity, 0) / self.total_rolls) * 100 if self.total_rolls > 0 else 0
            print(f"\nComparison for {rarity}:")
            print(f"  - Expected: {expected_percentage:.2f}%")
            print(f"  - Got: {actual_percentage:.2f}%")
