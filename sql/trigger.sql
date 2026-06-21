/* =====================================================
   FUNCTION
   Automatically updates listing statistics
===================================================== */

CREATE OR REPLACE FUNCTION update_listing_stats()

RETURNS TRIGGER AS
$$

BEGIN

    UPDATE listing_stats

    SET

        total_reviews =

        (
            SELECT COUNT(*)

            FROM reviews r

            WHERE r.listing_id = NEW.listing_id
        ),

        avg_rating =

        (
            SELECT AVG(rating)

            FROM reviews r

            WHERE r.listing_id = NEW.listing_id
        )

    WHERE listing_id = NEW.listing_id;

    RETURN NEW;

END;

$$ LANGUAGE plpgsql;



/* =====================================================
   TRIGGER
===================================================== */

DROP TRIGGER IF EXISTS trg_update_listing_stats ON reviews;

CREATE TRIGGER trg_update_listing_stats

AFTER INSERT ON reviews

FOR EACH ROW

EXECUTE FUNCTION update_listing_stats();