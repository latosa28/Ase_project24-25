-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS payment_db;
USE payment_db;  -- Select the database to use

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    card_number VARCHAR(16) NOT NULL,
    card_expiry VARCHAR(5) NOT NULL,
    card_cvc VARCHAR(3) NOT NULL,
    amount FLOAT NOT NULL,           -- Importo pagato in USD
    currency_amount FLOAT NOT NULL,  -- Quantità di valuta speciale (CURRENCY)
    status VARCHAR(20) NOT NULL,     -- Stato della transazione (successo/fallito)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Data di creazione della transazione
);