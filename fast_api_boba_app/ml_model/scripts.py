def get_boba_query(business_id):
    return f"""
    --sql
    WITH close_businesses AS (
        SELECT *               
        FROM businesses
        WHERE business_id = '{business_id}'
    )
    SELECT
        close_businesses.business_id,
        name,
        address,
        city,
        state,
        overall_star,
        review_count,
        review_id,
        reviews.stars,
        text,
        date
    FROM close_businesses
    LEFT JOIN reviews 
        ON close_businesses.business_id = reviews.business_id;
    """
