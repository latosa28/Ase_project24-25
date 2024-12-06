
# Ase_project24-25
## Get Started

Steps to get the project up and running:

1. **Ensure prerequisites are installed**  
   Before starting, make sure you have the following installed on your system:

   - **Docker** (version >= 20.10): [Docker Installation](https://docs.docker.com/get-docker/)  
   - **Docker Compose** (version >= 1.29): [Docker Compose Installation](https://docs.docker.com/compose/install/)

   To check the installed versions, use the following commands:

   ```bash
   docker --version
   docker-compose --version
   ```

2. **Clone the repository**  
   Clone the project repository and navigate to the main directory:

   ```bash
   git clone https://github.com/latosa28/Ase_project24-25
   cd Ase_project24-25/src
   ```

3. **Start the services**  
   Build and run all the containers with the command:

   ```bash
   docker-compose up --build
   ```

4. **Access the Services**  
   Once started, the services are accessible through the following ports:

   | Service               | Port   | Access URL                  |
   |-----------------------|--------|-----------------------------|
   | **Public API Gateway** | 5001   | https://localhost:5001       |
   | **Admin API Gateway**  | 5010   | https://localhost:5010       |

5. **Stop the services**  
   To stop all containers, run:

   ```bash
   docker-compose down
   ```

   This command stops and removes all containers, networks, and volumes created.

6. **Clean up containers**  
   If you want to remove all containers and persistent data (such as databases), run:

   ```bash
   docker-compose down --volumes
   ```


## TESTING

### Unit Test:
To run the unit tests for a single microservice, first import the JSON files for the microservices into Postman, which are located in the `docs/tests` folder.  
To start the individual microservice, navigate to the `src` folder in the terminal and run the following command:

```bash
docker-compose -f docker-compose.{microservice_name}.yml up --build
```

Then, run the imported collection in Postman.  
Finally, execute the following command to stop the microservice:

```bash
docker-compose -f docker-compose.{microservice_name}.yml down -v
```

### Integration Test:
To run the integration tests, first import the JSON file `Integration_test.postman_collection.json` into Postman, which is also located in the `docs/tests` folder.  
To start the application, navigate to the `src` folder in the terminal and run the following command:

```bash
docker-compose up --build
```

Then, run the imported collection in Postman.  
Finally, execute the following command to stop all services:

```bash
docker-compose down -v
```
### Performance Test:

To execute the performance tests located in the `docs/tests/performance_tests` folder, follow these steps:

1. **Start the application**  
   Navigate to the `src` directory and start the application with the command:

   ```bash
   docker-compose up --build
   ```

2. **Start Locust**  
   Open another terminal, navigate to the `docs/tests/performance_tests` directory, and start the Locust files with the command:

   ```bash
   locust -f {locustfile_name}.py
   ```

   - **`rarity_gacha_locustfile`**: implements only the roll operation.  
   - **`user_gacha_locustfile`**: includes all operations for managing gachas.

3. **Access the Locust interface**  
   Open a browser and go to the URL:

   ```plaintext
   http://localhost:8089/
   ```

4. **Set test parameters**  
   Once Locust is open, configure the required parameters, including:
   - Number of simultaneous users.
   - User spawn rate.
   - Test duration (configurable through *Advanced Options*).

   Start the test and monitor the results in real-time.

**Once finished, you can view the results from the terminal where you started locust.**

**Note:** After completing the test, remember to stop the containers with the command:

```bash
docker-compose down -v
```

