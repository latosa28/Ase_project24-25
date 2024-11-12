-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS collection_db;
USE collection_db;  -- Select the database to use

-- Create the item table if it does not already exist
CREATE TABLE IF NOT EXISTS item (
    id_item INT AUTO_INCREMENT PRIMARY KEY,          -- Unique ID for each item, auto-incremented
    rarity DECIMAL(5,2) NOT NULL CHECK (rarity >= 0 AND rarity <= 100),
    name VARCHAR(100) NOT NULL,                           -- Name of the item, cannot be null
    image_path VARCHAR(255) NOT NULL,             -- URL or path to the image, cannot be null
    UNIQUE (Name)                           -- Optional: Ensure that the item name is unique
);

-- Create the user_item table if it does not already exist
CREATE TABLE IF NOT EXISTS user_item (
    Id_istance  INT AUTO_INCREMENT PRIMARY KEY,       -- ID for the instance of the collection, this is the primary key
    Id_item INT NOT NULL,                             -- ID of the item, cannot be null (links to the item table)
    Id_user INT NOT NULL,                             -- ID of the user who owns the item, cannot be null
    Date_roll DATETIME NOT NULL,                      -- Date when the item was added to the collection, cannot be null
    FOREIGN KEY (Id_item) REFERENCES item(Id_item)    -- Foreign key linking to the item table
);


INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (1, 'Rayquaza', 0.05, '/collection_db/items_images/image1.png');
