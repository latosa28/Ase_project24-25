-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS ${DB_CURRENCY_NAME};
USE ${DB_CURRENCY_NAME};  -- Select the database to use

-- Create the currency table if it does not already exist
CREATE TABLE IF NOT EXISTS currency (
    Id_user INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each user, auto-incremented
    amount DECIMAL(10, 2) NOT NULL           -- Amount (e.g., balance or currency amount), cannot be null
);