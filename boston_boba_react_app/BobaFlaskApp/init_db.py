import sqlite3


def seed_businesses(db):
    """Initialize our businesses table using data from the yelp.db
    """    
    sqliteConnection = sqlite3.connect("../../yelp.db")
    cursor = sqliteConnection.cursor()
    query = """WITH close_businesses AS (SELECT 
                    business_id,
                    name,
                    address,
                    city,
                    state,
                    stars,
                    review_count,
                    distance_to_cambridge
                FROM businesses
                WHERE distance_to_cambridge < 10
                AND categories LIKE "%Bubble Tea%"
                )
                SELECT
                    close_businesses.business_id,
                    name,
                    address,
                    city,
                    state,
                    close_businesses.stars as overall_star,
                    review_count
                FROM close_businesses
                """

