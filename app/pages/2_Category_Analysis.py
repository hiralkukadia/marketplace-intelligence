import streamlit as st
import plotly.express as px
from db import run_query

st.set_page_config(layout="wide")

st.title("📦 Category Performance Analysis")

st.markdown("""
Compare categories by revenue, ratings, demand and marketplace opportunity.
""")

# ==========================
# CATEGORY OVERVIEW
# ==========================

query = """
SELECT
    c.category_name,

    COUNT(DISTINCT l.listing_id) AS listings,

    ROUND(AVG(ls.avg_rating),2) AS avg_rating,

    SUM(ls.total_sales) AS total_sales,

    ROUND(SUM(t.price_paid),2) AS revenue,

    SUM(ds.views) AS total_views

FROM categories c

JOIN listings l
ON c.category_id = l.category_id

JOIN listing_stats ls
ON l.listing_id = ls.listing_id

JOIN transactions t
ON l.listing_id = t.listing_id

JOIN demand_signals ds
ON l.listing_id = ds.listing_id

GROUP BY c.category_name
ORDER BY revenue DESC
"""

df = run_query(query)

# ==========================
# KPIs
# ==========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏆 Highest Revenue",
    df.iloc[0]["category_name"]
)

col2.metric(
    "⭐ Highest Rated",
    df.sort_values(
        "avg_rating",
        ascending=False
    ).iloc[0]["category_name"]
)

col3.metric(
    "🔥 Highest Demand",
    df.sort_values(
        "total_views",
        ascending=False
    ).iloc[0]["category_name"]
)

col4.metric(
    "📦 Categories",
    len(df)
)

st.divider()

# ==========================
# REVENUE
# ==========================

st.subheader("💰 Revenue by Category")

fig = px.bar(
    df,
    x="category_name",
    y="revenue",
    text="revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# DEMAND
# ==========================

st.subheader("👀 Demand by Category")

fig = px.bar(
    df,
    x="category_name",
    y="total_views",
    text="total_views"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# RATINGS
# ==========================

st.subheader("⭐ Average Rating by Category")

fig = px.bar(
    df,
    x="category_name",
    y="avg_rating",
    text="avg_rating"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# SALES VS RATINGS
# ==========================

st.subheader("📈 Sales vs Ratings")

fig = px.scatter(
    df,
    x="avg_rating",
    y="total_sales",
    size="revenue",
    color="category_name",
    hover_name="category_name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================
# OPPORTUNITY SCORE
# ==========================

st.subheader("🚀 Category Opportunity Score")

max_revenue = df["revenue"].max()
max_views = df["total_views"].max()
max_rating = df["avg_rating"].max()

df["opportunity_score"] = (
    (df["revenue"] / max_revenue) * 40 +
    (df["total_views"] / max_views) * 35 +
    (df["avg_rating"] / max_rating) * 25
)

opportunity = df.sort_values(
    "opportunity_score",
    ascending=False
)

st.dataframe(
    opportunity[
        [
            "category_name",
            "revenue",
            "total_views",
            "avg_rating",
            "opportunity_score"
        ]
    ],
    use_container_width=True
)

best = opportunity.iloc[0]

st.success(
    f"""
Recommended category to enter:

🏆 {best['category_name']}

Why?

• Highest combined opportunity score

• Strong demand

• Strong revenue

• Positive customer ratings
"""
)