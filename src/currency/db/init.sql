-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS currency_db;
USE currency_db;  -- Select the database to use

-- Create the currency table if it does not already exist
CREATE TABLE IF NOT EXISTS currency (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each user, auto-incremented
    amount DECIMAL(10, 2) NOT NULL           -- Amount (e.g., balance or currency amount), cannot be null
);