import streamlit as st
import pandas as pd

st.title("⚡ Query Performance")

before = pd.DataFrame({
    "Query":[
        "Demand vs Rating",
        "Revenue by Category",
        "Rating Segment Analysis"
    ],
    "Before(ms)":[
        99,
        186,
        37
    ]
})

after = pd.DataFrame({
    "Query":[
        "Demand vs Rating",
        "Revenue by Category",
        "Rating Segment Analysis"
    ],
    "After(ms)":[
        74,
        111,
        37
    ]
})

st.subheader("Performance Improvement")

merged = before.merge(after,on="Query")

merged["Improvement %"] = round(
    (
        (merged["Before(ms)"]-
         merged["After(ms)"])
         /
         merged["Before(ms)"]
    )*100,
    2
)

st.dataframe(merged,use_container_width=True)

st.bar_chart(
    merged.set_index("Query")[["Before(ms)","After(ms)"]]
)

st.success(
    "Indexes reduced execution time and improved query performance."
)