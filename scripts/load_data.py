import pandas as pd
import psycopg2

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------

conn = psycopg2.connect(
    dbname="marketplace",
    user="postgres",
    password="zda24b024",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

print("Connected to database successfully")

# ---------------------------------------------------
# SAFE CSV LOADER FUNCTION
# ---------------------------------------------------

def load_csv(table, file_path, columns):
    print(f"Loading {table}...")

    df = pd.read_csv(file_path)

    # remove duplicate primary keys
    df = df.drop_duplicates(subset=[columns[0]])

    for _, row in df.iterrows():

        values = []

        for col in columns:
            val = row[col]

            # convert numpy types to python native types
            if hasattr(val, "item"):
                val = val.item()

            # handle NaN values
            if pd.isna(val):
                val = None

            values.append(val)

        placeholders = ",".join(["%s"] * len(values))

        query = f"""
        INSERT INTO {table} VALUES ({placeholders})
        ON CONFLICT DO NOTHING
        """

        try:
            cur.execute(query, tuple(values))
        except Exception as e:
            print(f"Error inserting into {table}: {e}")

    conn.commit()
    print(f"Loaded {table} successfully\n")

# ---------------------------------------------------
# CORE DATA (REAL AIRBNB DATA)
# ---------------------------------------------------

load_csv(
    "locations",
    "data/processed/locations.csv",
    ["location_id", "city", "country"]
)

load_csv(
    "categories",
    "data/processed/categories.csv",
    ["category_id", "category_name"]
)

load_csv(
    "users",
    "data/processed/users.csv",
    ["user_id", "user_type", "join_date", "location_id"]
)

load_csv(
    "listings",
    "data/processed/listings.csv",
    ["listing_id", "seller_id", "category_id", "created_at"]
)

load_csv(
    "price_history",
    "data/processed/price_history.csv",
    ["price_id", "listing_id", "price", "timestamp"]
)

load_csv(
    "reviews",
    "data/processed/reviews.csv",
    ["review_id", "listing_id", "rating", "review_text", "timestamp"]
)

# ---------------------------------------------------
# SIMULATED DATA (ECONOMIC LAYER)
# ---------------------------------------------------

load_csv(
    "transactions",
    "data/simulated/transactions.csv",
    ["transaction_id", "buyer_id", "listing_id", "transaction_date", "price_paid"]
)

load_csv(
    "demand_signals",
    "data/simulated/demand_signals.csv",
    ["signal_id", "listing_id", "views", "wishlist_count", "time_period"]
)

load_csv(
    "user_behavior",
    "data/simulated/user_behavior.csv",
    ["behavior_id", "user_id", "listing_id", "event_type", "timestamp"]
)

load_csv(
    "listing_stats",
    "data/simulated/listing_stats.csv",
    ["listing_id", "avg_rating", "total_reviews", "total_sales"]
)

# ---------------------------------------------------
# CLOSE CONNECTION
# ---------------------------------------------------

cur.close()
conn.close()

print("ALL DATA LOADED SUCCESSFULLY")