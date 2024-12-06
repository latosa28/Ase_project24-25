import argparse
import subprocess
import os

services = [
    "auth",
    "collection",
    "account",
    "admin_account",
    "market",
    "currency",
    "payment",
    "api_gateway",
    "admin_api_gateway"
]

base_path = '../src/'


def run_pip_audit(service, fix=False):
    """Funzione per eseguire pip-audit su una cartella specifica"""
    try:
        print(f"Running pip-audit for {service}...")
        # Naviga nella directory del microservizio
        os.chdir(service)

        # Esegui pip-audit
        result = subprocess.run(
            ['pip-audit'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout)

        if fix:
            result = subprocess.run(
                ['pip-audit --fix'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(result.stdout)

    except Exception as e:
        print(f"An error occurred while running pip-audit on {service}: {e}")
    finally:
        # Torna alla directory iniziale
        os.chdir(base_path)


def main():
    # Crea un parser per gli argomenti da linea di comando
    parser = argparse.ArgumentParser(description="Run pip-audit on a list of microservices.")
    parser.add_argument(
        '--fix',
        action='store_true',
        help="Run pip-audit with the --fix option to automatically fix issues."
    )

    # Analizza gli argomenti della linea di comando
    args = parser.parse_args()

    os.chdir(base_path)
    for service in services:
        run_pip_audit(service, fix=args.fix)


if __name__ == '__main__':
    main()
