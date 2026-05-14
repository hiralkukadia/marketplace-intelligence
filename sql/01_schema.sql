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

CREATE TABLE Locations (
    location_id INT PRIMARY KEY,
    city TEXT,
    country TEXT
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY,
    category_name TEXT
);

CREATE TABLE Users (
    user_id BIGINT PRIMARY KEY,
    user_type TEXT,
    join_date DATE,
    location_id INT REFERENCES Locations(location_id)
);

CREATE TABLE Listings (
    listing_id BIGINT PRIMARY KEY,
    seller_id BIGINT REFERENCES Users(user_id),
    category_id INT REFERENCES Categories(category_id),
    created_at TIMESTAMP
);

CREATE TABLE Price_History (
    price_id INT PRIMARY KEY,
    listing_id BIGINT REFERENCES Listings(listing_id),
    price DECIMAL(10,2),
    timestamp TIMESTAMP
);

CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    buyer_id BIGINT REFERENCES Users(user_id),
    listing_id BIGINT REFERENCES Listings(listing_id),
    transaction_date TIMESTAMP,
    price_paid DECIMAL(10,2)
);

CREATE TABLE Reviews (
    review_id INT PRIMARY KEY,
    listing_id BIGINT REFERENCES Listings(listing_id),
    rating INT,
    review_text TEXT,
    timestamp TIMESTAMP
);

CREATE TABLE Listing_Stats (
    listing_id BIGINT PRIMARY KEY REFERENCES Listings(listing_id),
    avg_rating DECIMAL(3,2),
    total_reviews INT,
    total_sales INT
);

CREATE TABLE Demand_Signals (
    signal_id INT PRIMARY KEY,
    listing_id BIGINT REFERENCES Listings(listing_id),
    views INT,
    wishlist_count INT,
    time_period DATE
);

CREATE TABLE User_Behavior (
    behavior_id INT PRIMARY KEY,
    user_id BIGINT REFERENCES Users(user_id),
    listing_id BIGINT REFERENCES Listings(listing_id),
    event_type TEXT,
    timestamp TIMESTAMP
);