from locust import HttpUser, task, between
import random
import json
import time 

class RarityGachaTestUser(HttpUser):
    wait_time = between(0.1, 0.2)
    user_counter = 0
    successful_users = []  # Lista per raccogliere gli utenti che completano il flusso

    def on_start(self):
        """Initialize the user, log in and prepare necessary data."""
        self.__class__.user_counter += 1
        self.user_id = self.__class__.user_counter
        self.username = f"user_{self.user_id}"
        self.email = f"user_{self.user_id}@example.com"
        self.password = "password123"

        # Sleep to avoid server overload
        time.sleep(self.user_id * 1.5)

        # Creazione utente, login e aggiunta di fondi
        if not self.create_user():
            return  # Se fallisce la creazione dell'utente, esci

        if not self.login():
            return  # Se fallisce il login, esci

        if not self.add_funds(10000): 
            return  # Se fallisce l'aggiunta di fondi, esci

        self.rarity_counts = {
            "superultrarare": 0,
            "ultrarare": 0,
            "superrare": 0,
            "rare": 0,
            "common": 0
        }
        self.total_rolls = 0

        # Se tutte le operazioni sono state eseguite con successo, aggiungi l'utente alla lista
        self.__class__.successful_users.append(self)

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
        }, headers=self.headers, verify=False)  # Disable SSL verification

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
        if self not in self.__class__.successful_users:
            return  # Se l'utente non ha completato con successo, non stampare i risultati

        if self == self.__class__.successful_users[-1]:
            # Ordinare gli utenti per user_id
            sorted_users = sorted(self.__class__.successful_users, key=lambda u: u.user_id)

            print("\n--- Summary for all successful users ---")
            for user in sorted_users:
                print(f"\nResults for User {user.user_id}:")
                print(f"  Total Rolls: {user.total_rolls}")
                for rarity, count in user.rarity_counts.items():
                    percentage = (count / user.total_rolls) * 100 if user.total_rolls > 0 else 0
                    print(f"  {rarity}: {count} ({percentage:.2f}%)")

            # Confronto con la distribuzione prevista
            expected_distribution = {
                "superultrarare": 0.05,
                "ultrarare": 0.5,
                "superrare": 5.0,
                "rare": 40.0,
                "common": 54.45
            }

            print("\n--- Comparison with expected distribution ---")
            for user in sorted_users:
                print(f"\nResults for User {user.user_id}:")
                for rarity, expected_percentage in expected_distribution.items():
                    actual_percentage = (user.rarity_counts.get(rarity, 0) / user.total_rolls) * 100 if user.total_rolls > 0 else 0
                    print(f"  {rarity}: Expected {expected_percentage:.2f}%, Got {actual_percentage:.2f}%")
