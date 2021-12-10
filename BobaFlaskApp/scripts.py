def get_boba_query(business_id):
    return f"""WITH close_businesses AS (SELECT 
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
            AND business_id = '{business_id}'
            AND categories LIKE "%Bubble Tea%"
            )
            SELECT
                close_businesses.business_id,
                name,
                address,
                city,
                state,
                close_businesses.stars as overall_star,
                review_count,
                review_id,
                distance_to_cambridge,
                reviews.stars,
                text,
                date
            FROM close_businesses
            LEFT JOIN reviews 
                ON close_businesses.business_id = reviews.business_id
            """