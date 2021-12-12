def get_boba_query(business_id):
    return f"""WITH close_businesses AS (SELECT 
                business_id,
                name,
                address,
                city,
                state,
                stars,
                review_count
            FROM businesses
            WHERE business_id = '{business_id}'
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
                reviews.stars,
                text,
                date
            FROM close_businesses
            LEFT JOIN reviews 
                ON close_businesses.business_id = reviews.business_id
            """