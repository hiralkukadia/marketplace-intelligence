
-- =========================
-- MARKETPLACE INTELLIGENCE PLATFORM
-- FINAL STABLE SCHEMA (AIRBNB COMPATIBLE)
-- =========================

DROP TABLE IF EXISTS User_Behavior;
DROP TABLE IF EXISTS Demand_Signals;
DROP TABLE IF EXISTS Listing_Stats;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Price_History;
DROP TABLE IF EXISTS Listings;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Locations;

-- -------------------------
-- DOMAIN 1: MARKETPLACE
-- -------------------------

CREATE TABLE Locations (
    location_id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    country TEXT NOT NULL
);

CREATE TABLE Users (
    user_id BIGINT PRIMARY KEY,
    user_type TEXT NOT NULL CHECK (user_type IN ('buyer', 'seller')),
    join_date DATE NOT NULL,
    location_id INT REFERENCES Locations(location_id)
);

CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT UNIQUE NOT NULL
);

CREATE TABLE Listings (
    listing_id BIGINT PRIMARY KEY,
    seller_id BIGINT NOT NULL,
    category_id INT REFERENCES Categories(category_id),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE Price_History (
    price_id SERIAL PRIMARY KEY,
    listing_id BIGINT REFERENCES Listings(listing_id),
    price DECIMAL(10,2) NOT NULL CHECK (price > 0),
    timestamp TIMESTAMP NOT NULL
);

-- -------------------------
-- DOMAIN 2: TRUST SYSTEM
-- -------------------------

CREATE TABLE Transactions (
    transaction_id SERIAL PRIMARY KEY,
    buyer_id BIGINT REFERENCES Users(user_id),
    listing_id BIGINT REFERENCES Listings(listing_id),
    transaction_date TIMESTAMP NOT NULL,
    price_paid DECIMAL(10,2) NOT NULL
);

CREATE TABLE Reviews (
    review_id SERIAL PRIMARY KEY,
    listing_id BIGINT REFERENCES Listings(listing_id),
    rating INT CHECK (rating BETWEEN 1 AND 5),
    review_text TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE Listing_Stats (
    listing_id BIGINT PRIMARY KEY,
    avg_rating DECIMAL(10,2),
    total_reviews INT DEFAULT 0,
    total_sales INT DEFAULT 0
);

-- -------------------------
-- DOMAIN 3: DEMAND SYSTEM
-- -------------------------

CREATE TABLE Demand_Signals (
    signal_id SERIAL PRIMARY KEY,
    listing_id BIGINT REFERENCES Listings(listing_id),
    views INT,
    wishlist_count INT,
    time_period DATE
);

CREATE TABLE User_Behavior (
    behavior_id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES Users(user_id),
    listing_id BIGINT REFERENCES Listings(listing_id),
    event_type TEXT CHECK (event_type IN ('view','click','purchase')),
    timestamp TIMESTAMP
);