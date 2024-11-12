-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS collection_db;
USE collection_db;  -- Select the database to use

-- Create the item table if it does not already exist
CREATE TABLE IF NOT EXISTS item (
    id_item INT AUTO_INCREMENT PRIMARY KEY,          -- Unique ID for each item, auto-incremented
    rarity ENUM('superultrarare', 'ultrarare', 'superrare', 'rare', 'common') NOT NULL, -- Rarity as ENUM
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
VALUES (1, 'Alakazam', 'rare', '/collection_db/items_images/Alakazam.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (2, 'Articuno', 'ultrarare', '/collection_db/items_images/Articuno.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (3, 'Diglett', 'common', '/collection_db/items_images/Diglett.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (4, 'Eevee', 'rare', '/collection_db/items_images/Eevee.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (5, 'Growlithe', 'rare', '/collection_db/items_images/Growlithe.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (6, 'Gyarados', 'superrare', '/collection_db/items_images/Gyarados.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (6, 'Horsea', 'rare', '/collection_db/items_images/Horsea.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (7, 'Jigglypuff', 'common', '/collection_db/items_images/Jigglypuff.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (8, 'Lapras', 'superrare', '/collection_db/items_images/Lapras.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (9, 'Lugia', 'ultrarare', '/collection_db/items_images/Lugia.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (10, 'Machamp', 'superrare', '/collection_db/items_images/Machamp.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (11, 'Magmar', 'rare', '/collection_db/items_images/Magmar.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (12, 'Meowth', 'common', '/collection_db/items_images/Meowth.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (13, 'Mewtwo', 'superultrarare', '/collection_db/items_images/Mewtwo.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (14, 'Pidgey', 'common', '/collection_db/items_images/Pidgey.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (15, 'Poliwag', 'common', '/collection_db/items_images/Poliwag.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (15, 'Rattata', 'common', '/collection_db/items_images/Rattata.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (16, 'Rayquaza', 'superultrarare', '/collection_db/items_images/Rayquaza.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (17, 'Snorlax', 'superrare', '/collection_db/items_images/Snorlax.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (18, 'Tangela', 'rare', '/collection_db/items_images/Tangela.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (18, 'Zubat', 'common', '/collection_db/items_images/Zubat.png');

INSERT IGNORE INTO item (id_item, Name, rarity, image_path)
VALUES (18, 'Zygarde', 'ultrarare', '/collection_db/items_images/Zygarde.png');
