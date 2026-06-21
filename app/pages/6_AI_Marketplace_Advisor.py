import streamlit as st
from db import run_query

st.title("🤖 AI Marketplace Advisor")

st.markdown("""
Ask the system:

**'Which category should I sell in?'**

The advisor analyzes:

- Revenue
- Demand
- Ratings

and recommends the strongest category.
""")

if st.button("Generate Recommendation"):

    # ----------------------------
    # Highest Revenue Category
    # ----------------------------

    revenue_query = """
    SELECT
        c.category_name,
        SUM(t.price_paid) AS revenue
    FROM transactions t
    JOIN listings l
        ON t.listing_id = l.listing_id
    JOIN categories c
        ON l.category_id = c.category_id
    GROUP BY c.category_name
    ORDER BY revenue DESC
    LIMIT 1
    """

    revenue_df = run_query(revenue_query)

    top_revenue_category = revenue_df.iloc[0]["category_name"]
    top_revenue_value = revenue_df.iloc[0]["revenue"]

    # ----------------------------
    # Highest Demand Category
    # ----------------------------

    demand_query = """
    SELECT
        c.category_name,
        SUM(ds.views) AS total_views
    FROM demand_signals ds
    JOIN listings l
        ON ds.listing_id = l.listing_id
    JOIN categories c
        ON l.category_id = c.category_id
    GROUP BY c.category_name
    ORDER BY total_views DESC
    LIMIT 1
    """

    demand_df = run_query(demand_query)

    top_demand_category = demand_df.iloc[0]["category_name"]
    top_demand_value = demand_df.iloc[0]["total_views"]

    # ----------------------------
    # Best Rated Category
    # ----------------------------

    rating_query = """
    SELECT
        c.category_name,
        ROUND(AVG(ls.avg_rating),2) AS avg_rating
    FROM listing_stats ls
    JOIN listings l
        ON ls.listing_id = l.listing_id
    JOIN categories c
        ON l.category_id = c.category_id
    GROUP BY c.category_name
    ORDER BY avg_rating DESC
    LIMIT 1
    """

    rating_df = run_query(rating_query)

    top_rating_category = rating_df.iloc[0]["category_name"]
    top_rating_value = rating_df.iloc[0]["avg_rating"]

    # ----------------------------
    # Recommendation Logic
    # ----------------------------

    score = {}

    score[top_revenue_category] = score.get(top_revenue_category, 0) + 3
    score[top_demand_category] = score.get(top_demand_category, 0) + 2
    score[top_rating_category] = score.get(top_rating_category, 0) + 1

    recommended_category = max(score, key=score.get)

    st.subheader("📊 Marketplace Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Highest Revenue Category",
            top_revenue_category
        )

        st.write(
            f"Revenue: ${float(top_revenue_value):,.2f}"
        )

    with col2:
        st.metric(
            "Highest Demand Category",
            top_demand_category
        )

        st.write(
            f"Views: {int(top_demand_value):,}"
        )

    with col3:
        st.metric(
            "Best Rated Category",
            top_rating_category
        )

        st.write(
            f"Rating: {float(top_rating_value):.2f}"
        )

    st.divider()

    st.success(
        f"✅ Recommendation: Sell in '{recommended_category}'"
    )

    st.markdown(
        f"""
### Why?

The advisor compares marketplace performance across categories.

- Highest Revenue: **{top_revenue_category}**
- Highest Demand: **{top_demand_category}**
- Best Ratings: **{top_rating_category}**

Based on a weighted scoring model, the strongest opportunity is:

# 🏆 {recommended_category}

This category currently provides the best balance of:
- Customer demand
- Revenue potential
- Customer satisfaction
"""
    )

    st.divider()

    st.subheader("📈 Category Opportunity Ranking")

    ranking_query = """
    SELECT
        c.category_name,
        SUM(t.price_paid) AS revenue,
        SUM(ds.views) AS views,
        ROUND(AVG(ls.avg_rating),2) AS rating
    FROM categories c
    JOIN listings l
        ON c.category_id = l.category_id
    JOIN listing_stats ls
        ON l.listing_id = ls.listing_id
    JOIN demand_signals ds
        ON l.listing_id = ds.listing_id
    JOIN transactions t
        ON l.listing_id = t.listing_id
    GROUP BY c.category_name
    """

    rank_df = run_query(ranking_query)

    rank_df["revenue_score"] = (
        rank_df["revenue"] /
        rank_df["revenue"].max()
    )

    rank_df["views_score"] = (
        rank_df["views"] /
        rank_df["views"].max()
    )

    rank_df["rating_score"] = (
        rank_df["rating"] /
        rank_df["rating"].max()
    )

    rank_df["opportunity_score"] = (
        rank_df["revenue_score"] * 0.5 +
        rank_df["views_score"] * 0.3 +
        rank_df["rating_score"] * 0.2
    )

    rank_df = rank_df.sort_values(
        "opportunity_score",
        ascending=False
    )

    st.dataframe(
        rank_df[
            [
                "category_name",
                "revenue",
                "views",
                "rating",
                "opportunity_score"
            ]
        ],
        use_container_width=True
    )