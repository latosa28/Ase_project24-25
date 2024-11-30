import os
import subprocess

# Lista di microservizi e gateway
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

# Path base per i certificati
base_path = './secrets/'


# Funzione per creare i certificati
def generate_certificates(service_name, no_db_cert=False):
    cert_dir = os.path.join(base_path, service_name)
    os.makedirs(cert_dir, exist_ok=True)

    # esplicitato nel caso volessi cambiare i nomi
    cert_path = os.path.join(cert_dir, "cert.pem")
    key_path = os.path.join(cert_dir, "key.pem")

    # Generazione del certificato e della chiave con openssl
    command = [
        "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes", "-out", cert_path,
        "-keyout", key_path, "-days", "365", "-subj", f"/CN={service_name.upper()}"
    ]

    print(f"Generando certificato per {service_name}...")
    subprocess.run(command, check=True)

    if not no_db_cert:
        generate_db_certificates(service_name)


# Funzione per generare certificati per il DB (con SSL)
def generate_db_certificates(service_name):
    db_cert_dir = os.path.join(base_path, service_name)
    os.makedirs(db_cert_dir, exist_ok=True)

    db_cert_path = os.path.join(db_cert_dir, "db_cert.pem")
    db_key_path = os.path.join(db_cert_dir, "db_key.pem")

    # Generazione del certificato e della chiave con openssl per il DB
    command = [
        "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes", "-out", db_cert_path,
        "-keyout", db_key_path, "-days", "365", "-subj", f"/CN={service_name.upper()}_DB"
    ]

    print(f"Generando certificato per il DB di {service_name}...")
    subprocess.run(command, check=True)


# Funzione per generare il certificato CA (Certificate Authority)
def generate_ca_cert():
    ca_cert_dir = os.path.join(base_path, 'mysql')
    os.makedirs(ca_cert_dir, exist_ok=True)

    ca_cert_path = os.path.join(ca_cert_dir, "mysql_ca_cert.pem")

    # Generazione del certificato CA (self-signed)
    command = [
        "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes", "-out", ca_cert_path,
        "-keyout", ca_cert_path, "-days", "365", "-subj", "/CN=MySQL_CA"
    ]

    print("Generando certificato CA per MySQL...")
    subprocess.run(command, check=True)


# Funzione per generare una password sicura
def generate_db_password(service_name):
    # Lunghezza della password
    password_length = 16

    password = f'{service_name}_password'

    # Scrittura della password in un file
    password_file_path = os.path.join(base_path, service_name, 'db_password.txt')
    with open(password_file_path, 'w') as password_file:
        password_file.write(password)

    print(f"Password per {service_name} generata e salvata in {password_file_path}")
    return password


def generate_mysql_root_password():
    # password root sql uguale per tutti
    cert_dir = os.path.join(base_path, "mysql")
    os.makedirs(cert_dir, exist_ok=True)
    generate_db_password("mysql")


# Lista dei servizi per i quali non generiamo certificati DB
no_db_services = ["api_gateway", "admin_api_gateway", "auth"]

# Generazione dei certificati per ogni servizio
for service in services:
    no_db_serv = service in no_db_services
    generate_certificates(service, no_db_serv)
    if not no_db_serv:
        generate_db_password(service)

# Generazione password root mysql uguale per tutti
generate_mysql_root_password()
# Generazione del certificato CA per MySQL
generate_ca_cert()

print("Secrets generati con successo!")