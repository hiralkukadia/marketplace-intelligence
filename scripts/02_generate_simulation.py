import pandas as pd
import numpy as np
import os

processed_dir = "data/processed"
sim_dir = "data/simulated"

os.makedirs(sim_dir, exist_ok=True)

# Load processed datasets
listings = pd.read_csv(f"{processed_dir}/listings.csv")
users = pd.read_csv(f"{processed_dir}/users.csv")
reviews = pd.read_csv(f"{processed_dir}/reviews.csv")

np.random.seed(42)

# ----------------------------
# TRANSACTIONS
# ----------------------------

transactions = pd.DataFrame({
    "transaction_id": range(1, len(listings) + 1),
    "buyer_id": np.random.choice(users["user_id"], len(listings)),
    "listing_id": listings["listing_id"],
    "transaction_date": "2024-01-01",
    "price_paid": np.random.uniform(50, 500, len(listings)).round(2)
})

# ----------------------------
# DEMAND SIGNALS
# ----------------------------

demand_signals = pd.DataFrame({
    "signal_id": range(1, len(listings) + 1),
    "listing_id": listings["listing_id"],
    "views": np.random.randint(100, 5000, len(listings)),
    "wishlist_count": np.random.randint(10, 500, len(listings)),
    "time_period": "2024-01-01"
})

# ----------------------------
# USER BEHAVIOR
# ----------------------------

event_types = ["view", "click", "purchase"]

user_behavior = pd.DataFrame({
    "behavior_id": range(1, len(listings) + 1),
    "user_id": np.random.choice(users["user_id"], len(listings)),
    "listing_id": listings["listing_id"],
    "event_type": np.random.choice(event_types, len(listings)),
    "timestamp": "2024-01-01"
})

# ----------------------------
# LISTING STATS
# ----------------------------

listing_stats = reviews.groupby("listing_id").agg(
    avg_rating=("rating", "mean"),
    total_reviews=("rating", "count")
).reset_index()

listing_stats["total_sales"] = np.random.randint(
    1,
    100,
    len(listing_stats)
)

# Save
transactions.to_csv(f"{sim_dir}/transactions.csv", index=False)
demand_signals.to_csv(f"{sim_dir}/demand_signals.csv", index=False)
user_behavior.to_csv(f"{sim_dir}/user_behavior.csv", index=False)
listing_stats.to_csv(f"{sim_dir}/listing_stats.csv", index=False)

print("Simulation datasets generated successfully.")