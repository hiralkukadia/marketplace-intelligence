
\copy Locations(city, country) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/locations.csv' CSV HEADER;
\copy Categories(category_name) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/categories.csv' CSV HEADER;
\copy Users(user_id, user_type, join_date, location_id) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/users.csv' CSV HEADER;
\copy Listings(listing_id, seller_id, category_id, created_at) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/listings.csv' CSV HEADER;
\copy Price_History(price_id, listing_id, price, timestamp) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/price_history.csv' CSV HEADER;
\copy Transactions(transaction_id, buyer_id, listing_id, transaction_date, price_paid) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/transactions.csv' CSV HEADER;
\copy Reviews(review_id, listing_id, rating, review_text, timestamp) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/reviews.csv' CSV HEADER;
\copy Demand_Signals(signal_id, listing_id, views, wishlist_count, time_period) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/demand_signals.csv' CSV HEADER;
\copy User_Behavior(behavior_id, user_id, listing_id, event_type, timestamp) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/user_behavior.csv' CSV HEADER;
\copy Listing_Stats(listing_id, avg_rating, total_reviews, total_sales) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/listing_stats.csv' CSV HEADER;