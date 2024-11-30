import subprocess
import json
import os
import time


class PostmanTestRunner:
    def __init__(self, services: list[str]):
        """
        Inizializza il runner con una lista di servizi Docker.
        :param services: Lista dei nomi dei servizi Docker per cui eseguire i test
        """
        self.services = services

    def run_tests(self):
        """
        Esegui i test per tutti i servizi Docker passati.
        """
        for service in self.services:
            self.run_service_test(service)

    def run_service_test(self, service : str):
        """
        Esegui i test di un singolo servizio associato a una collezione Postman.
        :param service: Nome del servizio Docker
        """
        collection = f"../docs/tests/{service.capitalize()}_Test.postman_collection.json"

        # Controlla se il file della collezione esiste
        if not os.path.exists(collection):
            print(f"File collezione non trovato per il servizio: {service} ({collection})")
            return

        # Avvia i servizi Docker necessari per il test
        self.start_service(service)

        print(f"Inizio esecuzione della collezione per il servizio: {service} ({collection})")

        # Comando per eseguire il test con Newman
        command = ["newman", "run", collection]

        try:
            # Esegui il comando usando subprocess
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"Test completati con successo per il servizio: {service}")
                # Facoltativamente, analizzare i risultati JSON per ulteriori dettagli
                self.parse_newman_results(result.stdout)
            else:
                print(f"Errore nell'esecuzione dei test per il servizio: {service}")
                print(result.stderr)

        except Exception as e:
            print(f"Errore nell'esecuzione dei test: {e}")

        # Fermare i servizi Docker dopo i test
        self.stop_service(service)

    def start_service(self, service : str):

        print(f"Avvio il servizio Docker: {service}")
        command = ["docker-compose", "-f", f"./docker-compose.{service}.yml", "up", "--build", "-d"]
        try:
            subprocess.run(command, check=True)
            print("Servizi Docker avviati con successo.")
            time.sleep(5)  # Attendi qualche secondo che i servizi siano pronti
        except subprocess.CalledProcessError as e:
            print(f"Errore nell'avvio dei servizi Docker: {e}")
            exit(1)  # Uscire in caso di errore nell'avvio dei container

    def stop_service(self, service):
        """
        Esegui il comando docker-compose down per fermare i servizi.
        :param services: Lista dei nomi dei servizi Docker da fermare
        """
        print(f"Fermando il servizio Docker: {service}")
        command = ["docker-compose", "-f", f"./docker-compose.{service}.yml", "down", "-v"]
        try:
            subprocess.run(command, check=True)
            print("Servizio Docker fermati con successo.")
        except subprocess.CalledProcessError as e:
            print(f"Errore durante l'arresto del servizio Docker: {e}")

    def parse_newman_results(self, output):
        """
        Analizza i risultati JSON restituiti da Newman e stampa un report.
        :param output: Output JSON generato da Newman
        """
        try:
            result_json = json.loads(output)
            for run in result_json['run']['executions']:
                request_name = run['item']['name']
                if run['status'] == 'failed':
                    print(f"Errore nella richiesta: {request_name}")
                    print(f"Errore: {run['error']['message']}")
                else:
                    print(f"Test passato per la richiesta: {request_name}")

        except json.JSONDecodeError:
            print("Impossibile analizzare l'output JSON dei risultati di Newman")


# Esegui i test per una lista di servizi Docker
if __name__ == "__main__":
    services = ["market", "payment", "currency"]

    runner = PostmanTestRunner(services)
    runner.run_tests()
