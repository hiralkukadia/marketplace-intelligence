import streamlit as st
from db import run_query
from chatbot_engine import classify_question

st.title("🤖 Marketplace Analytics Chatbot")

st.markdown("""
Ask questions about the marketplace.

### Examples

- What category makes the most revenue?
- Which category has the highest demand?
- What is the average marketplace rating?
- Show top 10 sellers
- Show top revenue categories
- How many listings exist?
""")

question = st.text_input(
    "Ask a question"
)

if question:

    intent = classify_question(question)

    # ------------------------
    # Total Listings
    # ------------------------

    if intent == "listing":

        df = run_query("""
        SELECT COUNT(*) AS total
        FROM listings
        """)

        st.success(
            f"There are {int(df.iloc[0]['total']):,} listings."
        )

    # ------------------------
    # Average Rating
    # ------------------------

    elif intent == "rating":

        df = run_query("""
        SELECT ROUND(AVG(avg_rating),2) AS rating
        FROM listing_stats
        """)

        st.success(
            f"Marketplace average rating is {df.iloc[0]['rating']}."
        )

    # ------------------------
    # Revenue Leader
    # ------------------------

    elif intent == "revenue":

        df = run_query("""
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
        LIMIT 1
        """)

        st.success(
            f"{df.iloc[0]['category_name']} generates the highest revenue."
        )

        st.dataframe(df)

    # ------------------------
    # Highest Demand
    # ------------------------

    elif intent == "demand":

        df = run_query("""
        SELECT
            c.category_name,
            SUM(ds.views) AS views
        FROM demand_signals ds
        JOIN listings l
        ON ds.listing_id=l.listing_id
        JOIN categories c
        ON l.category_id=c.category_id
        GROUP BY c.category_name
        ORDER BY views DESC
        LIMIT 1
        """)

        st.success(
            f"{df.iloc[0]['category_name']} has the highest demand."
        )

        st.dataframe(df)

    # ------------------------
    # Top Sellers
    # ------------------------

    elif intent == "seller":

        df = run_query("""
        SELECT
            seller_id,
            SUM(ls.total_sales) AS sales
        FROM listings l
        JOIN listing_stats ls
        ON l.listing_id=ls.listing_id
        GROUP BY seller_id
        ORDER BY sales DESC
        LIMIT 10
        """)

        st.subheader("Top Sellers")

        st.dataframe(
            df,
            use_container_width=True
        )

    # ------------------------
    # Revenue Categories
    # ------------------------

    elif intent == "revenue_categories":

        df = run_query("""
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
        """)

        st.dataframe(
            df,
            use_container_width=True
        )

        st.bar_chart(
            df.set_index("category_name")
        )

    else:

        st.warning("""
I don't know how to answer that yet.

Try:

• What category makes the most revenue?

• Which category has the highest demand?

• Show top sellers

• Show revenue categories

• How many listings exist?

• What is the average rating?
""")