/* =====================================================
   INDEX FOR LISTING_STATS LOOKUPS
===================================================== */

CREATE INDEX idx_listing_stats_listing_id
ON listing_stats(listing_id);



/* =====================================================
   INDEX FOR DEMAND SIGNAL LOOKUPS
===================================================== */

CREATE INDEX idx_demand_signals_listing_id
ON demand_signals(listing_id);



/* =====================================================
   INDEX FOR TRANSACTION LOOKUPS
===================================================== */

CREATE INDEX idx_transactions_listing_id
ON transactions(listing_id);



/* =====================================================
   INDEX FOR CATEGORY LOOKUPS
===================================================== */

CREATE INDEX idx_listings_category_id
ON listings(category_id);



/* =====================================================
   INDEX FOR TRUST ANALYSIS
===================================================== */

CREATE INDEX idx_listing_stats_rating
ON listing_stats(avg_rating);