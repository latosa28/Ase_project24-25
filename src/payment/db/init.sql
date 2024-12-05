-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS payment_db;
USE payment_db;  -- Select the database to use

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_data VARCHAR(500) NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);