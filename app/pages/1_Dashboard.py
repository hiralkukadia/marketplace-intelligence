import streamlit as st
from db import run_query

st.title("📈 Marketplace Dashboard")

total_listings = run_query("""
SELECT COUNT(*) AS total
FROM listings
""")

total_sales = run_query("""
SELECT SUM(total_sales) AS sales
FROM listing_stats
""")

total_revenue = run_query("""
SELECT SUM(price_paid) AS revenue
FROM transactions
""")

avg_rating = run_query("""
SELECT ROUND(AVG(avg_rating),2) AS rating
FROM listing_stats
""")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Listings", f"{int(total_listings.iloc[0,0]):,}")
col2.metric("Sales", f"{int(total_sales.iloc[0,0]):,}")
col3.metric("Revenue", f"${float(total_revenue.iloc[0,0]):,.0f}")
col4.metric("Average Rating", avg_rating.iloc[0,0])

st.divider()

st.subheader("Revenue by Category")

query = """
SELECT
c.category_name,
SUM(t.price_paid) AS revenue
FROM transactions t
JOIN listings l
ON t.listing_id=l.listing_id
JOIN categories c
ON l.category_id=c.category_id
GROUP BY c.category_name
ORDER BY revenue DESC
"""

df = run_query(query)

st.bar_chart(df.set_index("category_name"))