from locust import HttpUser, task, between
import random
import json
import time


class RarityGachaTestUser(HttpUser):
    wait_time = between(0.1, 0.2)  # Tempo di attesa tra le richieste
    user_counter = 0  # Contatore per assegnare un ID univoco a ogni utente

    def on_start(self):
        """Inizializza l'utente, esegue il login e predispone i dati necessari."""
        self.__class__.user_counter += 1
        self.user_id = self.__class__.user_counter
        self.username = f"user_{self.user_id}"
        self.email = f"user_{self.user_id}@example.com"
        self.password = "password123"

        # Attendi brevemente per evitare di sovraccaricare il server
        time.sleep(self.user_id * 0.5)

        if not self.create_user():
            return  # Interrompe se la creazione fallisce

        if not self.login():
            return  # Interrompe se il login fallisce

        if not self.add_funds(10000): 
            return  # Interrompe se l'aggiunta di fondi fallisce

        # Inizializza le statistiche di raccolta
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
            print(f"Aggiunti {amount} currency all'utente {self.username}.")
            return True
        else:
            print(f"Errore nell'aggiunta di denaro per l'utente {self.username}: {response.text}")
            return False

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

    def on_stop(self):
        """Riassume i risultati ottenuti alla fine del test."""
        print(f"--- Riassunto statistiche finali Utente {self.user_id} ---")
        print(f"Totale roll effettuati: {self.total_rolls}")

        for rarity, count in self.rarity_counts.items():
            percentage = (count / self.total_rolls) * 100 if self.total_rolls > 0 else 0
            print(f"{rarity}: {count} ({percentage:.2f}%)")

        # Distribuzione attesa
        expected_distribution = {
            "superultrarare": 0.05,
            "ultrarare": 0.5,
            "superrare": 5.0,
            "rare": 40.0,
            "common": 54.45
        }

        # Confronto tra distribuzione attesa e reale
        for rarity, expected_percentage in expected_distribution.items():
            actual_percentage = (self.rarity_counts.get(rarity, 0) / self.total_rolls) * 100 if self.total_rolls > 0 else 0
            print(f"\nConfronto per {rarity}:")
            print(f"  - Atteso: {expected_percentage:.2f}%")
            print(f"  - Ottenuto: {actual_percentage:.2f}%")
