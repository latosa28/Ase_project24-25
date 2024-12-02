import subprocess
import os
import time

BASE_PATH = "../"


class PostmanTestRunner:
    def __init__(self, services: list[str]):
        self.services = services

    def run_tests(self):
        """
        Esegui i test per tutti i servizi Docker passati, seguiti dal test di integrazione.
        """
        for service in self.services:
            self.run_service_test(service)

        # Dopo aver eseguito i test sui singoli servizi, esegui il test di integrazione
        self.run_integration_test()

    def run_service_test(self, service: str):
        """
        Esegui i test di un singolo servizio associato a una collezione Postman.
        :param service: Nome del servizio Docker
        """
        collection_path = os.path.join(BASE_PATH, f"docs/tests/{service.capitalize()}_Test.postman_collection.json")

        # Controlla se il file della collezione esiste
        if not os.path.exists(collection_path):
            print(f"File collezione non trovato per il servizio: {service} ({collection_path})")
            return

        # Avvia i servizi Docker necessari per il test
        self.start_service(service)

        print(f"Inizio esecuzione della collezione per il servizio: {service} ({collection_path})")

        # Comando per eseguire il test con Newman
        command = ["newman", "run", collection_path, "--insecure"]

        try:
            # Esegui il comando usando subprocess
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)

        except Exception as e:
            print(f"Errore nell'esecuzione dei test: {e}")

        # Fermare i servizi Docker dopo i test
        self.stop_service(service)

    def start_service(self, service: str):
        """
        Avvia il servizio Docker per il servizio specificato.
        """
        print(f"Avvio il servizio Docker: {service}")
        command = ["docker-compose", "-f", f"{BASE_PATH}src/docker-compose.{service}.yml", "up", "--build", "-d"]
        try:
            subprocess.run(command, check=True)
            print("Servizi Docker avviati con successo.")
            time.sleep(5)
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'avvio dei servizi Docker: {e}")
            exit(1)  # Uscire in caso di errore nell'avvio dei container

    def stop_service(self, service):
        """
        Esegui il comando docker-compose down per fermare i servizi.
        :param service: Nome del servizio Docker da fermare
        """
        print(f"Fermando il servizio Docker: {service}")
        command = ["docker-compose", "-f", f"{BASE_PATH}src/docker-compose.{service}.yml", "down", "-v"]
        try:
            subprocess.run(command, check=True)
            print("Servizio Docker fermato con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'arresto del servizio Docker: {e}")

    def run_integration_test(self):
        """
        Esegui il test di integrazione dopo aver completato i test per i singoli servizi.
        """
        integration_collection_path = os.path.join(BASE_PATH, "docs/tests/Integration_Test.postman_collection.json")

        # Controlla se il file del test di integrazione esiste
        if not os.path.exists(integration_collection_path):
            print(f"File collezione di integrazione non trovato: {integration_collection_path}")
            return

        # Avvia tutti i servizi necessari per il test di integrazione
        self.start_integration_services()

        print(f"Inizio esecuzione del test di integrazione: {integration_collection_path}")

        # Comando per eseguire il test di integrazione con Newman
        command = ["newman", "run", integration_collection_path, "--insecure"]

        try:
            # Esegui il comando usando subprocess
            result = subprocess.run(command, capture_output=True, text=True)
            print(result.stdout)

        except Exception as e:
            print(f"Errore nell'esecuzione dei test di integrazione: {e}")

        # Fermare i servizi Docker dopo i test di integrazione
        self.stop_integration_services()

    def start_integration_services(self):
        """
        Avvia i servizi Docker necessari per il test di integrazione.
        """
        print("Avvio i servizi Docker per il test di integrazione")
        command = ["docker-compose", "-f", f"{BASE_PATH}src/docker-compose.yml", "up", "--build", "-d"]
        try:
            subprocess.run(command, check=True)
            print("Servizi Docker per il test di integrazione avviati con successo.")
            time.sleep(15)  # Attendi qualche secondo che i servizi siano pronti
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'avvio dei servizi Docker per il test di integrazione: {e}")
            exit(1)  # Uscire in caso di errore nell'avvio dei container

    def stop_integration_services(self):
        """
        Fermare i servizi Docker dopo il test di integrazione.
        """
        print("Fermando i servizi Docker per il test di integrazione")
        command = ["docker-compose", "-f", f"{BASE_PATH}src/docker-compose.yml", "down", "-v"]
        try:
            subprocess.run(command, check=True)
            print("Servizi Docker per il test di integrazione fermati con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'arresto dei servizi Docker per il test di integrazione: {e}")


# Esegui i test per una lista di servizi Docker
if __name__ == "__main__":
    services = ["market", "currency", "payment", "collection", "account", "auth"]  # Lista dei servizi da testare

    runner = PostmanTestRunner(services)
    runner.run_tests()
