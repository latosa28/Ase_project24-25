-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS admin_db;
USE admin_db;  -- Select the database to use

-- Create the admin_account table if it does not already exist
CREATE TABLE IF NOT EXISTS admin_account (
    Id_user INT AUTO_INCREMENT PRIMARY KEY,           -- Unique ID for each admin user, auto-incremented
    Username VARCHAR(100) NOT NULL,                     -- Username for the admin user, cannot be null
    Email VARCHAR(255) NOT NULL,                       -- Email for the admin user, cannot be null
    Password VARCHAR(255) NOT NULL,                     -- Password for the admin user, cannot be null
    UNIQUE (Username),                                  -- Unique index on the Username field to avoid duplicates
    UNIQUE (Email)                                      -- Unique index on the Email field to avoid duplicates
);