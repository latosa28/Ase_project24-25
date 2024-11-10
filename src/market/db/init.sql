-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS ${DB_MARKET_NAME};
USE ${DB_MARKET_NAME};  -- Select the database to use

-- Create the market table if it does not already exist
CREATE TABLE IF NOT EXISTS market (
    Id_market INT AUTO_INCREMENT PRIMARY KEY,        -- Unique ID for each market record, auto-incremented
    Id_istance INT NOT NULL,                          -- ID for the auction instance, cannot be null
    Id_user_seller INT NOT NULL,                      -- ID of the seller user, cannot be null
    Id_user_buyer INT,                                -- ID of the buyer user (can be null, if no buyer yet)
    start_date DATETIME NOT NULL,                     -- Start date and time of the auction, cannot be null
    end_date DATETIME NOT NULL,                       -- End date and time of the auction, cannot be null
    bid DECIMAL(10, 2) NOT NULL                       -- The current bid amount, cannot be null
);