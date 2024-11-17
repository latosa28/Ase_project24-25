-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS market_db;
USE market_db;  -- Select the database to use

-- Create the market table if it does not already exist
CREATE TABLE IF NOT EXISTS market (
    market_id INT AUTO_INCREMENT PRIMARY KEY,        -- Unique ID for each market record, auto-incremented
    istance_id INT NOT NULL,                          -- ID for the auction instance, cannot be null
    seller_user_id INT NOT NULL,                      -- ID of the seller user, cannot be null
    buyer_user_id INT,                                -- ID of the buyer user (can be null, if no buyer yet)
    start_date TIMESTAMP NOT NULL,                     -- Start date and time of the auction, cannot be null
    end_date TIMESTAMP NOT NULL,                       -- End date and time of the auction, cannot be null
    status ENUM('open', 'closed') NOT NULL,           -- Auction status
    bid DECIMAL(10, 2) NOT NULL                       -- The current bid amount, cannot be null
);