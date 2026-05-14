import os
import shutil
import random
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import kagglehub

# ----------------------------------------
# REPRODUCIBILITY
# ----------------------------------------

np.random.seed(42)
random.seed(42)

# ----------------------------------------
# PATHS
# ----------------------------------------

RAW_DIR = "../data/raw/"
OUT_DIR = "../data/"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ----------------------------------------
# DOWNLOAD AIRBNB DATASET
# ----------------------------------------

def ensure_airbnb_data():

    listings_path = os.path.join(RAW_DIR, "listings.csv")
    reviews_path = os.path.join(RAW_DIR, "reviews.csv")

    # Skip download if already exists
    if os.path.exists(listings_path):
        print("Airbnb listings already present.")
        return

    print("Downloading dataset...")

    dataset_path = kagglehub.dataset_download(
        "arianazmoudeh/airbnbopendata"
    )

    csv_files = [
        f for f in os.listdir(dataset_path)
        if f.endswith(".csv")
    ]

    if len(csv_files) == 0:
        raise RuntimeError("No CSV files found.")

    print("CSV files found:", csv_files)

    # Use first CSV as listings
    first_csv = csv_files[0]

    shutil.copy(
        os.path.join(dataset_path, first_csv),
        listings_path
    )

    print(f"Using {first_csv} as listings.csv")

    # Optional reviews file
    for f in csv_files:
        if "review" in f.lower():

            shutil.copy(
                os.path.join(dataset_path, f),
                reviews_path
            )

            print(f"Using {f} as reviews.csv")
            break

    print("Download complete.")

# ----------------------------------------
# RUN DOWNLOAD
# ----------------------------------------

ensure_airbnb_data()

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

listings_raw = pd.read_csv(
    os.path.join(RAW_DIR, "listings.csv"),
    low_memory=False
)

# Normalize column names
listings_raw.columns = (
    listings_raw.columns
    .str.lower()
    .str.replace(" ", "_")
)

print("Columns in dataset:")
print(listings_raw.columns.tolist())

# ----------------------------------------
# DYNAMIC COLUMN MAPPING
# ----------------------------------------

def find_column(possible_names):

    for col in listings_raw.columns:

        for name in possible_names:

            if name in col:
                return col

    return None

col_id = find_column(["id"])
col_host = find_column(["host"])
col_loc = find_column(["neighbourhood", "location"])
col_cat = find_column(["room", "property"])
col_price = find_column(["price"])

print("\nMapped columns:")
print(col_id, col_host, col_loc, col_cat, col_price)

if not all([
    col_id,
    col_host,
    col_loc,
    col_cat,
    col_price
]):
    raise RuntimeError(
        "Could not map required columns."
    )

# ----------------------------------------
# CLEAN LISTINGS
# ----------------------------------------

listings = listings_raw[
    [
        col_id,
        col_host,
        col_loc,
        col_cat,
        col_price
    ]
].dropna().copy()

listings.columns = [
    "listing_id",
    "seller_id",
    "location_name",
    "category_name",
    "price"
]

# Clean price column
listings["price"] = (
    listings["price"]
    .astype(str)
    .replace(r"[\$,]", "", regex=True)
)

listings["price"] = pd.to_numeric(
    listings["price"],
    errors="coerce"
)

listings = listings.dropna(subset=["price"])

# ----------------------------------------
# LIMIT DATASET SIZE
# ----------------------------------------

# Important for performance
listings = listings.head(2000)

print("\nListings cleaned:", len(listings))

# ----------------------------------------
# LOCATIONS TABLE
# ----------------------------------------

locations = (
    listings[["location_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

locations["location_id"] = (
    locations.index + 1
)

locations["city"] = locations["location_name"]
locations["country"] = "USA"

locations = locations[
    [
        "location_id",
        "city",
        "country"
    ]
]

# Merge back
listings = listings.merge(
    locations,
    left_on="location_name",
    right_on="city"
)

# ----------------------------------------
# CATEGORIES TABLE
# ----------------------------------------

categories = (
    listings[["category_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

categories["category_id"] = (
    categories.index + 1
)

# Merge back
listings = listings.merge(
    categories,
    on="category_name"
)

# ----------------------------------------
# FINAL LISTINGS TABLE
# ----------------------------------------

listings["created_at"] = "2021-01-01"

listings_final = listings[
    [
        "listing_id",
        "seller_id",
        "category_id",
        "created_at"
    ]
]

# ----------------------------------------
# USERS TABLE
# ----------------------------------------

# Sellers from Airbnb
sellers = listings[
    ["seller_id"]
].drop_duplicates()

sellers.columns = ["user_id"]

sellers["user_type"] = "seller"
sellers["join_date"] = "2020-01-01"
sellers["location_id"] = 1

# Simulated buyers
buyers = pd.DataFrame({

    "user_id": range(100000, 101200),

    "user_type": "buyer",

    "join_date": "2021-01-01",

    "location_id": 1
})

users = pd.concat(
    [sellers, buyers],
    ignore_index=True
)

print("Users created:", len(users))

# ----------------------------------------
# REVIEWS TABLE (SIMULATED)
# ----------------------------------------

reviews = []

review_id = 1

for listing_id in listings_final["listing_id"]:

    num_reviews = random.randint(5, 15)

    for _ in range(num_reviews):

        reviews.append([

            review_id,

            listing_id,

            random.randint(3, 5),

            "Simulated review",

            "2022-01-01"

        ])

        review_id += 1

reviews = pd.DataFrame(
    reviews,
    columns=[
        "review_id",
        "listing_id",
        "rating",
        "review_text",
        "timestamp"
    ]
)

print("Reviews generated:", len(reviews))

# ----------------------------------------
# TRANSACTIONS TABLE
# ----------------------------------------

transactions = []

transaction_id = 1

buyer_ids = buyers["user_id"].tolist()

for i in range(len(listings_final)):

    listing_id = listings_final.iloc[i]["listing_id"]

    price = listings.iloc[i]["price"]

    rating = np.random.uniform(3, 5)

    # Economic logic:
    # higher rating -> more sales
    # higher price -> fewer sales

    num_transactions = max(
        1,
        int((rating * 2 - price / 100) * 5)
    )

    for _ in range(num_transactions):

        transactions.append([

            transaction_id,

            random.choice(buyer_ids),

            listing_id,

            "2022-01-01",

            round(
                max(
                    1,
                    price + random.uniform(-10, 10)
                ),
                2
            )

        ])

        transaction_id += 1

transactions = pd.DataFrame(
    transactions,
    columns=[
        "transaction_id",
        "buyer_id",
        "listing_id",
        "transaction_date",
        "price_paid"
    ]
)

print("Transactions generated:", len(transactions))

# ----------------------------------------
# PRICE HISTORY TABLE
# ----------------------------------------

price_history = []

price_id = 1

for i in range(len(listings_final)):

    listing_id = listings_final.iloc[i]["listing_id"]

    base_price = listings.iloc[i]["price"]

    for j in range(5):

        price_history.append([

            price_id,

            listing_id,

            round(
                max(
                    1,
                    base_price + random.uniform(-20, 20)
                ),
                2
            ),

            datetime(2021, 1, 1) +
            timedelta(days=j * 30)

        ])

        price_id += 1

price_history = pd.DataFrame(
    price_history,
    columns=[
        "price_id",
        "listing_id",
        "price",
        "timestamp"
    ]
)

print("Price history rows:", len(price_history))

# ----------------------------------------
# DEMAND SIGNALS TABLE
# ----------------------------------------

demand_signals = []

signal_id = 1

for i in range(len(listings_final)):

    listing_id = listings_final.iloc[i]["listing_id"]

    price = listings.iloc[i]["price"]

    rating = np.random.uniform(3, 5)

    # Economic relationship
    views = int(
        200 +
        (rating * 50) -
        (price * 0.5)
    )

    wishlist = int(views * 0.2)

    demand_signals.append([

        signal_id,

        listing_id,

        max(0, views),

        max(0, wishlist),

        "2022-01-01"

    ])

    signal_id += 1

demand_signals = pd.DataFrame(
    demand_signals,
    columns=[
        "signal_id",
        "listing_id",
        "views",
        "wishlist_count",
        "time_period"
    ]
)

print("Demand rows:", len(demand_signals))

# ----------------------------------------
# USER BEHAVIOR TABLE
# ----------------------------------------

behavior = []

behavior_id = 1

all_users = users["user_id"].tolist()

for listing_id in listings_final["listing_id"]:

    for _ in range(30):

        behavior.append([

            behavior_id,

            random.choice(all_users),

            listing_id,

            "view",

            "2022-01-01"

        ])

        behavior_id += 1

behavior = pd.DataFrame(
    behavior,
    columns=[
        "behavior_id",
        "user_id",
        "listing_id",
        "event_type",
        "timestamp"
    ]
)

print("Behavior rows generated:", len(behavior))

# ----------------------------------------
# LISTING STATS TABLE
# ----------------------------------------

sales = (
    transactions
    .groupby("listing_id")
    .size()
    .reset_index(name="total_sales")
)

ratings = (
    reviews
    .groupby("listing_id")["rating"]
    .mean()
    .reset_index(name="avg_rating")
)

listing_stats = pd.merge(
    sales,
    ratings,
    on="listing_id"
)

listing_stats["total_reviews"] = (
    listing_stats["listing_id"]
    .map(
        reviews
        .groupby("listing_id")
        .size()
    )
)

print("Listing stats rows:", len(listing_stats))

# ----------------------------------------
# SAVE CSV FILES
# ----------------------------------------

print("\nSaving CSV files...")

locations.to_csv(
    OUT_DIR + "locations.csv",
    index=False
)

categories.to_csv(
    OUT_DIR + "categories.csv",
    index=False
)

users.to_csv(
    OUT_DIR + "users.csv",
    index=False
)

listings_final.to_csv(
    OUT_DIR + "listings.csv",
    index=False
)

reviews.to_csv(
    OUT_DIR + "reviews.csv",
    index=False
)

transactions.to_csv(
    OUT_DIR + "transactions.csv",
    index=False
)

price_history.to_csv(
    OUT_DIR + "price_history.csv",
    index=False
)

demand_signals.to_csv(
    OUT_DIR + "demand_signals.csv",
    index=False
)

behavior.to_csv(
    OUT_DIR + "user_behavior.csv",
    index=False
)

listing_stats.to_csv(
    OUT_DIR + "listing_stats.csv",
    index=False
)

print("\nSUCCESS: All data generated.")