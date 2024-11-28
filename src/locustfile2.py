from locust import HttpUser, task, between
import random
import json
import math
import logging

class GachaTestUser(HttpUser):
    wait_time = between(0.1, 0.2)
    user_counter = 0  # Contatore statico per ID univoci

    def on_start(self):
        """Inizializza l'utente e la sua collezione."""
        self.__class__.user_counter += 1
        self.user_id = self.__class__.user_counter
        self.username = f"user_{self.user_id}"
        self.email = f"user_{self.user_id}@example.com"
        self.password = "password123"

        # Crea e autentica un nuovo utente
        if not self.create_user():
            return  # Se la creazione dell'utente fallisce, termina

        if not self.login():
            return  # Se il login fallisce, termina

        # Aggiungi soldi al saldo dell'utente
        if not self.add_funds(1000):  # Ad esempio, aggiungiamo 100 unità di denaro
            return  # Se l'aggiunta di denaro fallisce, termina

        self.rarity_counts = {
            "superultrarare": 0,
            "ultrarare": 0,
            "superrare": 0,
            "rare": 0,
            "common": 0
        }
        self.total_rolls = 0

    def create_user(self):
        """Crea un nuovo utente con dati univoci."""
        response = self.client.post("/user", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        })

        if response.status_code == 201:
            print(f"Utente {self.username} creato con successo.")
            return True
        else:
            print(f"Errore nella creazione dell'utente {self.username}: {response.text}")
            return False

    def login(self):
        """Effettua il login dell'utente per ottenere un token."""
        response = self.client.post("/user/auth", json={
            "username": self.username,
            "password": self.password
        })

        if response.status_code == 200:
            self.headers = {
                "Authorization": f"Bearer {response.json()['token']}"
            }
            print(f"Utente {self.username} loggato con successo.")
            return True
        else:
            print(f"Errore nel login dell'utente {self.username}: {response.text}")
            return False

    def add_funds(self, amount):
        """Aggiungi denaro al saldo dell'utente."""
        response = self.client.post(f"/user/{self.user_id}/payment", json={
            "card_number": "4111111111111111",
            "card_expiry": "12/26",
            "card_cvc": "123",
            "amount": amount
        })

        if response.status_code == 200:
            print(f"Aggiunti {amount} soldi all'utente {self.username}.")
            return True
        else:
            print(f"Errore nell'aggiunta di denaro per l'utente {self.username}: {response.text}")
            return False

    def get_instance_id(self):
        """Recupera un ID di istanza casuale dalla collezione dell'utente."""
        response = self.client.get(f"/user/{self.user_id}/mycollection", headers=self.headers)
        if response.status_code == 200:
            collection = response.json()
            if collection:
                return random.choice(collection)["instance_id"]

    @task(3)
    def roll_gacha(self):
        """Simula un roll gacha."""
        response = self.client.put(f"/user/{self.user_id}/roll", headers=self.headers)
        if response.status_code == 201:
            self.total_rolls += 1
            try:
                rarity = response.json().get("rarity")
                if rarity in self.rarity_counts:
                    self.rarity_counts[rarity] += 1
            except json.JSONDecodeError:
                print(f"Errore nel decodificare la risposta JSON per l'utente {self.user_id}.")
        else:
            print(f"Roll fallito per utente {self.user_id}. Status: {response.status_code}")

    @task(1)
    def view_collection(self):
        """Visualizza la collezione dell'utente."""
        response = self.client.get(f"/user/{self.user_id}/mycollection", headers=self.headers)
        
        # Verifica se la risposta contiene una collezione non vuota
        collection = response.json()  # Supponiamo che la risposta sia in formato JSON
        if not collection:
            print(f"La collezione dell'utente {self.user_id} è vuota o malformata.")
        else:
            print(f"Collezione dell'utente {self.user_id}: {len(collection)} oggetti trovati.")

    @task(1)
    def get_item_instance(self):
        """Visualizza i dettagli di un'istanza di oggetto."""
        instance_id = self.get_instance_id()
        if instance_id:
            response = self.client.get(f"/user/{self.user_id}/instance/{instance_id}", headers=self.headers)
            if response.status_code != 200:
                print(f"Errore nel recupero dell'istanza {instance_id}: {response.status_code}")
        else:
            print("Nessuna istanza disponibile per l'utente.")

       
