# Ase_project24-25
## Get Started

Passaggi per avviare il progetto
1. Assicurati di avere i prerequisiti installati
Prima di iniziare, verifica di avere installato sul tuo sistema:

Docker (versione >= 20.10): Installazione Docker
Docker Compose (versione >= 1.29): Installazione Docker Compose
Per controllare le versioni installate, usa i seguenti comandi:

docker --version
docker-compose --version

2. Clona la repository
Clona la repository del progetto e accedi alla directory principale:

git clone https://github.com/latosa28/Ase_project24-25
cd nome-repository

3. Avvia i servizi
Costruisci ed esegui tutti i container con il comando:

docker-compose up --build

4.Accesso ai Servizi
Una volta avviati, i servizi sono accessibili tramite le seguenti porte:

Servizio	        Porta	Accesso
Public API Gateway	5001	http://localhost:5001
Admin API Gateway	5010	http://localhost:5010

5.Arrestare i servizi
Per fermare tutti i container, esegui:

docker-compose down
Questo comando arresta ed elimina tutti i container, le reti e i volumi creati.

Pulizia dei container
Se desideri rimuovere tutti i container e i dati persistenti (come i database), esegui:

docker-compose down --volumes

