<<<<<<< HEAD
# Marketplace Intelligence Platform: Trust, Pricing, and Demand Dynamics
#github link - https://github.com/hiralkukadia/marketplace-intelligence

## Project Overview

This project is an advanced database analytics platform designed to study how trust, pricing, and demand interact within peer-to-peer digital marketplaces.

The platform combines:
- real Airbnb marketplace data
- simulated behavioral marketplace activity
- SQL analytics
- economic analysis concepts

The project investigates the following research questions:

1. Do higher ratings allow sellers to charge higher prices?
2. Does demand respond more strongly to trust or price?
3. Do highly rated listings generate more sales?
4. Are there winner-takes-all effects in platform marketplaces?
5. How does user behavior influence conversion rates?

This project was developed for the Z2004 Database Management Systems course under Track C: Advanced Schema and Analytics Platform.


# Technologies Used

| Technology | Purpose |
|---|---|
| PostgreSQL | Database Management System |
| Python | Data cleaning and simulation |
| Pandas | Data manipulation |
| KaggleHub | Airbnb dataset download |
| SQL | Data querying and analytics |
| VS Code | Development environment |


# Dataset Source

Real marketplace data was obtained from the Airbnb Open Data dataset available on Kaggle.

Dataset:
- Airbnb Open Data

The dataset provides:
- listing prices
- room types
- locations
- review counts
- host information

Additional marketplace activity was simulated to model:
- transactions
- demand signals
- user behavior
- conversion funnels

This hybrid approach combines realism with analytical flexibility.


# Folder Structure

```plaintext
marketplace-intelligence/
│
├── data/
│   ├── raw_airbnb/
│   │   └── airbnb.csv
│   │
│   ├── processed/
│   │   ├── locations.csv
│   │   ├── categories.csv
│   │   ├── users.csv
│   │   ├── listings.csv
│   │   └── price_history.csv
│   │
│   └── simulated/
│       ├── transactions.csv
│       ├── reviews.csv
│       ├── demand_signals.csv
│       ├── user_behavior.csv
│       └── listing_stats.csv
│
├── scripts/
│   ├── 01_clean_airbnb.py
│   ├── 02_generate_simulated_data.py
│   └── load_data.py
│
├── sql/
│   ├── schema.sql
│   ├── queries.sql
│   └── indexes.sql
│
├── results/
│   └── query_results.txt
│
└── README.md