-- Create the database if it does not already exist
CREATE DATABASE IF NOT EXISTS account_db;
USE account_db;  -- Select the database to use

-- Create user table if it does not already exist
CREATE TABLE IF NOT EXISTS user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,  -- Unique ID for each user, auto-incremented
    username VARCHAR(50) NOT NULL,           -- Username, must be unique and not null
    email VARCHAR(100) NOT NULL,             -- User's email, must be unique and not null
    password VARCHAR(255) NOT NULL,          -- Password (hashed), must not be null
    UNIQUE (username),                      -- Unique index on the Username field to avoid duplicates
    UNIQUE (email)                          -- Unique index on the Email field to avoid duplicates
);