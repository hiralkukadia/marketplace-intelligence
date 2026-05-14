import pandas as pd
import numpy as np
import os

RAW_FILE = "data/raw_airbnb/listings.csv"

processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

print("Loading Airbnb dataset...")

df = pd.read_csv(RAW_FILE, low_memory=False)

print("\nACTUAL DATASET COLUMNS:")
print(df.columns.tolist())

# ---------------------------------------------------
# STANDARDIZE COLUMN NAMES
# ---------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nSTANDARDIZED COLUMNS:")
print(df.columns.tolist())

# ---------------------------------------------------
# COLUMN MAPPING
# ---------------------------------------------------

listing_col = "id"
seller_col = "host_id"
city_col = "neighbourhood_group"
category_col = "room_type"
rating_col = "review_rate_number"
price_col = "price"

required_cols = [
    listing_col,
    seller_col,
    city_col,
    category_col,
    rating_col,
    price_col
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    raise Exception(f"Missing required columns: {missing}")

print("\nCOLUMN MAPPING SUCCESSFUL")

# ---------------------------------------------------
# KEEP REQUIRED COLUMNS
# ---------------------------------------------------

df = df[required_cols]

# Rename columns
df = df.rename(columns={
    listing_col: "listing_id",
    seller_col: "seller_id",
    city_col: "city",
    category_col: "category_name",
    rating_col: "rating",
    price_col: "price"
})

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------

# Remove missing rows
df = df.dropna()

# Convert IDs
df["listing_id"] = pd.to_numeric(df["listing_id"], errors="coerce")
df["seller_id"] = pd.to_numeric(df["seller_id"], errors="coerce")

# Clean price
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Ratings
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["rating"] = df["rating"].fillna(4)

# Drop bad rows
df = df.dropna(subset=["listing_id", "seller_id", "price"])

# Convert types
df["listing_id"] = df["listing_id"].astype("int64")
df["seller_id"] = df["seller_id"].astype("int64")

# ---------------------------------------------------
# LOCATIONS
# ---------------------------------------------------

locations = pd.DataFrame({
    "location_id": range(1, df["city"].nunique() + 1),
    "city": df["city"].unique(),
    "country": "USA"
})

city_map = dict(zip(locations["city"], locations["location_id"]))

# ---------------------------------------------------
# CATEGORIES
# ---------------------------------------------------

categories = pd.DataFrame({
    "category_id": range(1, df["category_name"].nunique() + 1),
    "category_name": df["category_name"].unique()
})

cat_map = dict(zip(categories["category_name"], categories["category_id"]))

# ---------------------------------------------------
# USERS
# ---------------------------------------------------

users = pd.DataFrame({
    "user_id": df["seller_id"].unique()
})

users["user_type"] = "seller"
users["join_date"] = "2023-01-01"

users["location_id"] = np.random.choice(
    locations["location_id"],
    len(users)
)

# ---------------------------------------------------
# LISTINGS
# ---------------------------------------------------

listings = pd.DataFrame({
    "listing_id": df["listing_id"],
    "seller_id": df["seller_id"],
    "category_id": df["category_name"].map(cat_map),
    "created_at": "2024-01-01"
})

# ---------------------------------------------------
# PRICE HISTORY
# ---------------------------------------------------

price_history = pd.DataFrame({
    "price_id": range(1, len(df) + 1),
    "listing_id": df["listing_id"],
    "price": df["price"],
    "timestamp": "2024-01-01"
})

# ---------------------------------------------------
# REVIEWS
# ---------------------------------------------------

reviews = pd.DataFrame({
    "review_id": range(1, len(df) + 1),
    "listing_id": df["listing_id"],
    "rating": df["rating"].round().astype(int),
    "review_text": "Auto-generated review",
    "timestamp": "2024-01-01"
})

# ---------------------------------------------------
# SAVE FILES
# ---------------------------------------------------

locations.to_csv(f"{processed_dir}/locations.csv", index=False)
categories.to_csv(f"{processed_dir}/categories.csv", index=False)
users.to_csv(f"{processed_dir}/users.csv", index=False)
listings.to_csv(f"{processed_dir}/listings.csv", index=False)
price_history.to_csv(f"{processed_dir}/price_history.csv", index=False)
reviews.to_csv(f"{processed_dir}/reviews.csv", index=False)

print("\nCore datasets generated successfully.")