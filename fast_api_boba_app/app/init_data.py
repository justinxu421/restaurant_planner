import logging
import sqlite3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    pass


def init_businesses(c, conn):
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


def init_reviews(c, conn):
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


def main() -> None:
    # TODO: in the future, make this less hacky with a cloud based implementation (PostgresSQL)
    # read from a copy of yelp_db into boba_data_db to initialize our data

    conn = sqlite3.connect("yelp.db", check_same_thread=False)
    c = conn.cursor()
    c.execute("ATTACH DATABASE 'boba_data.db' AS boba_db")

    logger.info("Creating initial data")
    init_businesses(c, conn)
    logger.info("Finished initializing businesses")
    init_reviews(c, conn)
    logger.info("Finished initializing reviews")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
