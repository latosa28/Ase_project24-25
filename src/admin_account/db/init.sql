-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS admin_db;
USE admin_db;  -- Select the database to use

-- Create the admin_account table if it does not already exist
CREATE TABLE IF NOT EXISTS admin_account (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,           -- Unique ID for each admin user, auto-incremented
    username VARCHAR(100) NOT NULL,                     -- Username for the admin user, cannot be null
    email VARCHAR(255) NOT NULL,                       -- Email for the admin user, cannot be null
    password VARCHAR(255) NOT NULL,                     -- Password for the admin user, cannot be null
    UNIQUE (username),                                  -- Unique index on the Username field to avoid duplicates
    UNIQUE (email)                                      -- Unique index on the Email field to avoid duplicates
);