from locust import HttpUser, task, between
import random
import json
import time


class GachaTestUser(HttpUser):
    wait_time = between(0.5, 0.6)
    user_counter = 0  # Contatore statico per ID univoci
    successful_users = []

    def on_start(self):
        """Inizializza l'utente e configura i dati necessari."""
        self.__class__.user_counter += 1
        self.user_id = self.__class__.user_counter
        self.username = f"user_{self.user_id}"
        self.email = f"user_{self.user_id}@example.com"
        self.password = "password123"

        time.sleep(self.user_id * 1.5)

        # Crea e autentica un nuovo utente
        if not self.create_user():
            return
        if not self.login():
            return
        if not self.add_funds(10000):
            return

        # Inizializza statistiche locali
        self.rarity_counts = {
            "superultrarare": 0,
            "ultrarare": 0,
            "superrare": 0,
            "rare": 0,
            "common": 0
        }
        self.total_rolls = 0
        self.__class__.successful_users.append(self)

    def create_user(self):
        """Create a new user with unique data."""
        response = self.client.post("/user", json={
            "username": self.username,
            "email": self.email,
            "password": self.password
        }, verify=False)  # Disabilita verifica SSL
        if response.status_code == 201:
            print(f"Utente {self.username} creato con successo.")
            return True
        else:
            print(f"Errore nella creazione dell'utente {self.username}: {response.text}")
            return False

    def login(self):
        """Effettua il login per ottenere il token di autorizzazione."""
        response = self.client.post("/user/auth", json={
            "username": self.username,
            "password": self.password,
            "grant_type": "password"  # Aggiunto nuovo campo
        }, verify=False)  # Disabilita verifica SSL
        if response.status_code == 200:
            self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}  # Usa access_token
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
        }, headers=self.headers, verify=False)  # Disabilita verifica SSL
        if response.status_code == 200:
            print(f"Aggiunti {amount} soldi all'utente {self.username}.")
            return True
        else:
            print(f"Errore nell'aggiunta di denaro per l'utente {self.username}: {response.text}")
            return False

    def get_instance_id(self):
        """Recupera un ID di istanza casuale dalla collezione dell'utente."""
        response = self.client.get(f"/user/{self.user_id}/mycollection", headers=self.headers,verify=False)
        if response.status_code == 200:
            collection = response.json()
            if collection:
                return random.choice(collection)["instance_id"]

    @task(3)
    def roll_gacha(self):
        """Simula un roll gacha."""
        response = self.client.put(f"/user/{self.user_id}/roll", headers=self.headers, verify=False)  # Disabilita verifica SSL
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
    def view_my_collection(self):
        """Visualizza la collezione personale dell'utente."""
        self.client.get(f"/user/{self.user_id}/mycollection", headers=self.headers, verify=False)  # Disabilita verifica SSL

    @task(1)
    def view_system_collection(self):
        """Recupera la collezione globale del sistema."""
        self.client.get(f"/user/{self.user_id}/collection", headers=self.headers, verify=False)  # Disabilita verifica SSL

    @task(1)
    def get_item_details(self):
        """Recupera i dettagli di un Pokémon specifico dalla collezione globale."""
        # Recupera la collezione globale
        response = self.client.get(f"/user/{self.user_id}/collection", headers=self.headers, verify=False)  # Disabilita verifica SSL
        if response.status_code == 200:
            system_collection = response.json()
            if system_collection:
                # Scegli un Pokémon casuale e ottieni i suoi dettagli
                item_id = random.choice(system_collection)["item_id"]
                self.client.get(f"/user/{self.user_id}/item/{item_id}", headers=self.headers, verify=False)  # Disabilita verifica SSL

    def on_stop(self):
        """Riassume i risultati al termine del test."""
        if self not in self.__class__.successful_users:
            return  # Se l'utente non ha completato con successo, non stampare i risultati
        
        if self == self.__class__.successful_users[-1]:
            # Ordinare gli utenti per user_id
            sorted_users = sorted(self.__class__.successful_users, key=lambda u: u.user_id)

            # Stampa i risultati solo per gli utenti che hanno completato correttamente tutto il flusso
            for user in sorted_users:
                print(f"\n--- Risultati Utente {user.user_id} ---")
                print(f"Roll Totali: {user.total_rolls}")
                for rarity, count in user.rarity_counts.items():
                    print(f"{rarity.capitalize()}: {count}")
