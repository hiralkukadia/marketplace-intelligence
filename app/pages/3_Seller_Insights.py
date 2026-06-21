import streamlit as st
import pandas as pd
import plotly.express as px
from db import run_query

st.set_page_config(layout="wide")

st.title("👤 Seller Performance Dashboard")

st.markdown("""
Analyze seller performance, sales, ratings and marketplace dominance.
""")

# ==================================================
# TOP SELLERS
# ==================================================

st.header("🏆 Top Performing Sellers")

query = """
SELECT
    l.seller_id,
    COUNT(l.listing_id) AS listings,
    ROUND(AVG(ls.avg_rating),2) AS avg_rating,
    SUM(ls.total_sales) AS total_sales
FROM listings l
JOIN listing_stats ls
ON l.listing_id = ls.listing_id
GROUP BY l.seller_id
ORDER BY total_sales DESC
LIMIT 20;
"""

df = run_query(query)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Top Seller",
        int(df.iloc[0]["seller_id"])
    )

with col2:
    st.metric(
        "Highest Sales",
        f"{int(df['total_sales'].max()):,}"
    )

with col3:
    st.metric(
        "Average Seller Rating",
        round(df["avg_rating"].mean(),2)
    )

st.dataframe(df, use_container_width=True)

# ==================================================
# SALES CHART
# ==================================================

st.subheader("💰 Top Sellers by Sales")

fig = px.bar(
    df,
    x="seller_id",
    y="total_sales",
    text="total_sales",
    title="Top 20 Sellers by Sales"
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# RATINGS CHART
# ==================================================

st.subheader("⭐ Seller Ratings")

fig2 = px.scatter(
    df,
    x="avg_rating",
    y="total_sales",
    size="listings",
    hover_data=["seller_id"],
    title="Rating vs Sales"
)

st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# MARKET SHARE
# ==================================================

st.header("📊 Seller Market Share")

market_query = """
SELECT
    seller_id,
    SUM(total_sales) AS sales
FROM listings l
JOIN listing_stats ls
ON l.listing_id = ls.listing_id
GROUP BY seller_id
ORDER BY sales DESC
LIMIT 10;
"""

market_df = run_query(market_query)

fig3 = px.pie(
    market_df,
    names="seller_id",
    values="sales",
    title="Top 10 Seller Market Share"
)

st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# HIDDEN GEMS
# ==================================================

st.header("💎 Hidden Gem Sellers")

gem_query = """
SELECT
    l.seller_id,
    ROUND(AVG(ls.avg_rating),2) AS rating,
    SUM(ls.total_sales) AS sales
FROM listings l
JOIN listing_stats ls
ON l.listing_id = ls.listing_id
GROUP BY l.seller_id
HAVING AVG(ls.avg_rating) > 4.5
ORDER BY sales DESC
LIMIT 15;
"""

gems = run_query(gem_query)

st.dataframe(gems, use_container_width=True)

st.success(
    "These sellers maintain excellent ratings while still generating strong sales."
)

# ==================================================
# BUSINESS INSIGHTS
# ==================================================

st.header("🧠 Marketplace Insights")

best_seller = df.iloc[0]["seller_id"]
best_sales = int(df.iloc[0]["total_sales"])

st.info(f"""
Top marketplace seller is **Seller {best_seller}**
with approximately **{best_sales:,} sales**.

Key observations:

• Higher rated sellers generally achieve higher sales.

• A small number of sellers control a large portion of marketplace sales.

• Several sellers maintain ratings above 4.5 while generating significant revenue, indicating strong customer satisfaction.

• New sellers should study the strategies used by top-performing sellers.
""")