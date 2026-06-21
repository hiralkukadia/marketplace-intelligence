import streamlit as st
from db import run_query

st.title("🔥 Demand Analysis")

query = """
SELECT
c.category_name,
SUM(ds.views) AS total_views,
SUM(ds.wishlist_count) AS wishlist
FROM demand_signals ds
JOIN listings l
ON ds.listing_id=l.listing_id
JOIN categories c
ON l.category_id=c.category_id
GROUP BY c.category_name
ORDER BY total_views DESC
"""

df = run_query(query)

st.dataframe(df,use_container_width=True)

st.subheader("Marketplace Demand")

st.bar_chart(
    df.set_index("category_name")["total_views"]
)

st.subheader("Wishlist Interest")

st.bar_chart(
    df.set_index("category_name")["wishlist"]
)