-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS ${DB_COLLECTION_NAME};
USE ${DB_COLLECTION_NAME};  -- Select the database to use

-- Create the item table if it does not already exist
CREATE TABLE IF NOT EXISTS item (
    Id_item INT AUTO_INCREMENT PRIMARY KEY,          -- Unique ID for each item, auto-incremented
    Rarity VARCHAR(50) NOT NULL,                      -- Rarity of the item, cannot be null
    Characteristics TEXT NOT NULL                     -- Characteristics of the item, cannot be null
);

-- Create the user_item table if it does not already exist
CREATE TABLE IF NOT EXISTS user_item (
    Id_istance INT PRIMARY KEY,                       -- ID for the instance of the collection, this is the primary key
    Id_item INT NOT NULL,                             -- ID of the item, cannot be null (links to the item table)
    Id_user INT NOT NULL,                             -- ID of the user who owns the item, cannot be null
    Date_roll DATETIME NOT NULL,                      -- Date when the item was added to the collection, cannot be null
    FOREIGN KEY (Id_item) REFERENCES item(Id_item)   -- Foreign key linking to the item table
);