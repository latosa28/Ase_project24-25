-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS ${DB_ACCOUNT_NAME};
USE ${DB_ACCOUNT_NAME};  -- Select the database to use

-- Create user table if it does not already exist
CREATE TABLE IF NOT EXISTS user (
    Id_user INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each user, auto-incremented
    Username VARCHAR(50) NOT NULL,           -- Username, must be unique and not null
    Email VARCHAR(100) NOT NULL,             -- User's email, must be unique and not null
    Password VARCHAR(255) NOT NULL,          -- Password (hashed), must not be null
    UNIQUE (Username),                      -- Unique index on the Username field to avoid duplicates
    UNIQUE (Email)                          -- Unique index on the Email field to avoid duplicates
);