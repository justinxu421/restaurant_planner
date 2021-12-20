import logging

# from app.db.init_db import init_db
# from app.db.session import SessionLocal
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    # db = SessionLocal()
    # init_db(db)
    pass


def main() -> None:
    conn = sqlite3.connect("../yelp.db")
    c = conn.cursor()
    c.execute("ATTACH DATABASE '../boba_data.db' AS boba_db")

    query_business = """INSERT INTO 
                            boba_db.businesses (
                                business_id,
                                name,
                                address,
                                city,
                                state,
                                overall_star,
                                review_count
                            )
                        SELECT
                            business_id,
                            name,
                            address,
                            city,
                            state,
                            stars as overall_star,
                            review_count
                        FROM
                            businesses
                        WHERE
                            distance_to_cambridge < 100
                            AND categories LIKE "%Bubble Tea%"
                    """
    c.execute(query_business).fetchall()
    conn.commit()

    query_reviews = """INSERT INTO 
                        boba_db.reviews (
                            review_id,
                            user_id,
                            business_id,
                            stars,
                            useful,
                            funny,
                            cool,
                            text,
                            date,
                            text_length
                        )
                        SELECT 
                            review_id,
                            user_id,
                            reviews.business_id,
                            stars,
                            useful,
                            funny,
                            cool,
                            text,
                            date,
                            text_length
                        FROM reviews 
                        INNER JOIN boba_db.businesses
                        ON boba_db.businesses.business_id = reviews.business_id
                    """
    c.execute(query_reviews).fetchall()
    conn.commit()

    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
