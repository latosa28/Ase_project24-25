-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS payment_db;
USE payment_db;  -- Select the database to use

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount FLOAT NOT NULL,           -- Importo pagato in USD
    currency_amount FLOAT NOT NULL,  -- Quantità di valuta speciale (CURRENCY)
    status VARCHAR(20) NOT NULL,     -- Stato della transazione (successo/fallito)
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data di creazione della transazione
);