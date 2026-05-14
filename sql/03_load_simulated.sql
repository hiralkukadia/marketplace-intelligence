\copy transactions(transaction_id,buyer_id,listing_id,transaction_date,price_paid) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/simulated/transactions.csv' DELIMITER ',' CSV HEADER;

\copy demand_signals(signal_id,listing_id,views,wishlist_count,time_period) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/simulated/demand_signals.csv' DELIMITER ',' CSV HEADER;

\copy user_behavior(behavior_id,user_id,listing_id,event_type,timestamp) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/simulated/user_behavior.csv' DELIMITER ',' CSV HEADER;

\copy listing_stats(listing_id,avg_rating,total_reviews,total_sales) FROM 'C:/Users/USER/OneDrive/Desktop/marketplace-intelligence/data/simulated/listing_stats.csv' DELIMITER ',' CSV HEADER;