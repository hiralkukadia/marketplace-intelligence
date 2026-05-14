-- =========================================================
-- MARKETPLACE INTELLIGENCE PLATFORM
-- QUERIES.SQL
-- Track C - Advanced Analytics Queries
-- =========================================================



-- =========================================================
-- QUERY 1
-- Average Price by Listing Category
-- Aggregation + Join
-- =========================================================

SELECT 
    c.category_name,
    ROUND(AVG(ph.price), 2) AS avg_price
FROM listings l
JOIN categories c 
    ON l.category_id = c.category_id
JOIN price_history ph 
    ON l.listing_id = ph.listing_id
GROUP BY c.category_name
ORDER BY avg_price DESC;



-- =========================================================
-- QUERY 2
-- Average Rating by Category
-- Aggregation + Join
-- =========================================================

SELECT 
    c.category_name,
    ROUND(AVG(ls.avg_rating), 2) AS avg_rating
FROM listing_stats ls
JOIN listings l 
    ON ls.listing_id = l.listing_id
JOIN categories c 
    ON l.category_id = c.category_id
GROUP BY c.category_name
ORDER BY avg_rating DESC;



-- =========================================================
-- QUERY 3
-- Rating Groups vs Average Price
-- =========================================================

SELECT
    CASE
        WHEN ls.avg_rating < 2 THEN 'Poor'
        WHEN ls.avg_rating BETWEEN 2 AND 3 THEN 'Average'
        WHEN ls.avg_rating BETWEEN 3 AND 4 THEN 'Good'
        ELSE 'Excellent'
    END AS rating_group,

    ROUND(AVG(ph.price), 2) AS avg_price

FROM listing_stats ls
JOIN price_history ph
    ON ls.listing_id = ph.listing_id

GROUP BY rating_group
ORDER BY avg_price DESC;



-- =========================================================
-- QUERY 4
-- Rating Groups vs Demand
-- =========================================================

SELECT
    CASE
        WHEN ls.avg_rating < 2 THEN 'Poor'
        WHEN ls.avg_rating BETWEEN 2 AND 3 THEN 'Average'
        WHEN ls.avg_rating BETWEEN 3 AND 4 THEN 'Good'
        ELSE 'Excellent'
    END AS rating_group,

    SUM(ds.views) AS total_views

FROM listing_stats ls
JOIN demand_signals ds
    ON ls.listing_id = ds.listing_id

GROUP BY rating_group
ORDER BY total_views DESC;



-- =========================================================
-- QUERY 5
-- Price Range vs Demand
-- =========================================================

SELECT
    CASE
        WHEN ph.price < 50 THEN 'Low Price'
        WHEN ph.price BETWEEN 50 AND 150 THEN 'Medium Price'
        ELSE 'High Price'
    END AS price_range,

    SUM(ds.views) AS total_views

FROM price_history ph
JOIN demand_signals ds
    ON ph.listing_id = ds.listing_id

GROUP BY price_range
ORDER BY total_views DESC;



-- =========================================================
-- QUERY 6
-- Listings per Category
-- =========================================================

SELECT
    c.category_name,
    COUNT(*) AS total_listings
FROM listings l
JOIN categories c
    ON l.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_listings DESC;



-- =========================================================
-- QUERY 7
-- Seller Concentration by Category
-- =========================================================

SELECT
    c.category_name,
    COUNT(l.listing_id) AS total_listings,
    COUNT(DISTINCT l.seller_id) AS unique_sellers
FROM listings l
JOIN categories c
    ON l.category_id = c.category_id
GROUP BY c.category_name
ORDER BY total_listings DESC;



-- =========================================================
-- QUERY 8
-- Rating Groups vs Average Sales
-- CTE
-- =========================================================

WITH rating_sales AS (
    SELECT 
        listing_id,
        avg_rating,
        total_sales
    FROM listing_stats
)

SELECT 
    CASE
        WHEN avg_rating < 2 THEN 'Poor'
        WHEN avg_rating BETWEEN 2 AND 3 THEN 'Average'
        WHEN avg_rating BETWEEN 3 AND 4 THEN 'Good'
        ELSE 'Excellent'
    END AS rating_group,

    ROUND(AVG(total_sales), 2) AS avg_sales

FROM rating_sales
GROUP BY rating_group
ORDER BY avg_sales DESC;



-- =========================================================
-- QUERY 9
-- Average Marketplace Demand
-- CTE
-- =========================================================

WITH demand AS (
    SELECT 
        listing_id,
        SUM(views) AS total_views
    FROM demand_signals
    GROUP BY listing_id
)

SELECT 
    ROUND(AVG(total_views), 2) AS avg_marketplace_views
FROM demand;



-- =========================================================
-- QUERY 10
-- Top 10 Listings by Market Share
-- Window Function
-- =========================================================

SELECT
    listing_id,
    total_sales,

    ROUND(
        total_sales * 100.0 /
        SUM(total_sales) OVER (),
        2
    ) AS market_share_percentage,

    RANK() OVER (
        ORDER BY total_sales DESC
    ) AS sales_rank

FROM listing_stats

ORDER BY total_sales DESC
LIMIT 10;



-- =========================================================
-- QUERY 11
-- Top Rated Listings
-- Window Function
-- =========================================================

SELECT
    listing_id,
    avg_rating,

    RANK() OVER (
        ORDER BY avg_rating DESC
    ) AS rating_rank

FROM listing_stats

ORDER BY avg_rating DESC
LIMIT 10;



-- =========================================================
-- QUERY 12
-- Cumulative Marketplace Sales
-- Window Function
-- =========================================================

SELECT
    listing_id,
    total_sales,

    SUM(total_sales) OVER (
        ORDER BY total_sales DESC
    ) AS cumulative_sales

FROM listing_stats

ORDER BY total_sales DESC
LIMIT 15;



-- =========================================================
-- QUERY 13
-- Highest Conversion Categories
-- =========================================================

SELECT
    c.category_name,

    ROUND(
        SUM(CASE WHEN ub.event_type = 'purchase' THEN 1 ELSE 0 END)::NUMERIC
        /
        COUNT(*),
        4
    ) AS conversion_rate

FROM user_behavior ub

JOIN listings l
    ON ub.listing_id = l.listing_id

JOIN categories c
    ON l.category_id = c.category_id

GROUP BY c.category_name
ORDER BY conversion_rate DESC;



-- =========================================================
-- QUERY 14
-- Low Rated Listings Still Receiving High Demand
-- =========================================================

SELECT
    CASE
        WHEN ls.avg_rating < 2 THEN 'Poor'
        WHEN ls.avg_rating BETWEEN 2 AND 3 THEN 'Average'
        ELSE 'Above Average'
    END AS rating_group,

    ROUND(AVG(ds.views), 2) AS avg_views

FROM listing_stats ls
JOIN demand_signals ds
    ON ls.listing_id = ds.listing_id

WHERE ls.avg_rating < 3

GROUP BY rating_group
ORDER BY avg_views DESC;



-- =========================================================
-- QUERY 15
-- Price Range vs Average Views
-- =========================================================

SELECT
    CASE
        WHEN ph.price < 50 THEN 'Low Price'
        WHEN ph.price BETWEEN 50 AND 150 THEN 'Medium Price'
        ELSE 'High Price'
    END AS price_range,

    ROUND(AVG(ds.views), 2) AS avg_views

FROM price_history ph
JOIN demand_signals ds
    ON ph.listing_id = ds.listing_id

GROUP BY price_range
ORDER BY avg_views DESC;



-- =========================================================
-- QUERY 16
-- Top 10 Most Viewed Listings
-- =========================================================

SELECT
    listing_id,
    SUM(views) AS total_views
FROM demand_signals
GROUP BY listing_id
ORDER BY total_views DESC
LIMIT 10;



-- =========================================================
-- QUERY 17
-- Top Revenue Generating Listings
-- =========================================================

SELECT
    listing_id,
    ROUND(SUM(price_paid), 2) AS revenue
FROM transactions
GROUP BY listing_id
ORDER BY revenue DESC
LIMIT 10;



-- =========================================================
-- QUERY 18
-- Rating Groups vs Revenue
-- =========================================================

SELECT
    CASE
        WHEN ls.avg_rating < 2 THEN 'Poor'
        WHEN ls.avg_rating BETWEEN 2 AND 3 THEN 'Average'
        WHEN ls.avg_rating BETWEEN 3 AND 4 THEN 'Good'
        ELSE 'Excellent'
    END AS rating_group,

    ROUND(SUM(t.price_paid), 2) AS total_revenue

FROM listing_stats ls
JOIN transactions t
    ON ls.listing_id = t.listing_id

GROUP BY rating_group
ORDER BY total_revenue DESC;



-- =========================================================
-- QUERY 19
-- Category Market Share
-- Window Function
-- =========================================================

SELECT
    c.category_name,

    SUM(ls.total_sales) AS category_sales,

    ROUND(
        SUM(ls.total_sales) * 100.0 /
        SUM(SUM(ls.total_sales)) OVER (),
        2
    ) AS market_share

FROM listing_stats ls

JOIN listings l
    ON ls.listing_id = l.listing_id

JOIN categories c
    ON l.category_id = c.category_id

GROUP BY c.category_name
ORDER BY market_share DESC;



-- =========================================================
-- QUERY 20
-- Demand vs Sales Relationship
-- =========================================================

SELECT
    CASE
        WHEN ds.views < 500 THEN 'Low Demand'
        WHEN ds.views BETWEEN 500 AND 1500 THEN 'Medium Demand'
        ELSE 'High Demand'
    END AS demand_level,

    ROUND(AVG(ls.total_sales), 2) AS avg_sales

FROM demand_signals ds

JOIN listing_stats ls
    ON ds.listing_id = ls.listing_id

GROUP BY demand_level
ORDER BY avg_sales DESC;



-- =========================================================
-- QUERY 21
-- Listings Above Average Price
-- Subquery
-- =========================================================

SELECT
    listing_id,
    price
FROM price_history
WHERE price > (
    SELECT AVG(price)
    FROM price_history
)
ORDER BY price DESC
LIMIT 10;



-- =========================================================
-- QUERY 22
-- Listings With Above Average Sales
-- Subquery
-- =========================================================

SELECT
    listing_id,
    total_sales
FROM listing_stats
WHERE total_sales > (
    SELECT AVG(total_sales)
    FROM listing_stats
)
ORDER BY total_sales DESC
LIMIT 10;