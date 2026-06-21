import psycopg2
import pandas as pd

DB_CONFIG = {
    "host": "localhost",
    "database": "marketplace",
    "user": "postgres",
    "password": "zda24b024"
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def run_query(query):
    conn = get_connection()

    df = pd.read_sql(query, conn)

    conn.close()

    return df