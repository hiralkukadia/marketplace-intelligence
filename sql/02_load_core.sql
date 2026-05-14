\copy locations(location_id, city, country)
FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/processed/locations.csv'
DELIMITER ','
CSV HEADER;

\copy categories(category_id, category_name)
FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/processed/categories.csv'
DELIMITER ','
CSV HEADER;

\copy users(user_id, user_type, join_date, location_id)
FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/processed/users.csv'
DELIMITER ','
CSV HEADER;

\copy listings(listing_id, seller_id, category_id, created_at)
FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/processed/listings.csv'
DELIMITER ','
CSV HEADER;

\copy price_history(price_id, listing_id, price, timestamp)
FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/processed/price_history.csv'
DELIMITER ','
CSV HEADER;

\copy reviews(review_id, listing_id, rating, review_text, timestamp)
FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/processed/reviews.csv'
DELIMITER ','
CSV HEADER;