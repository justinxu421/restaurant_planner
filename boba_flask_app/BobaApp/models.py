from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BostonBobaBusiness(db.Model):
    __tablename__ = "boston_boba_businesses"
    business_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    overall_star = db.Column(db.Float)
    review_count = db.Column(db.Integer)

    def __init__(
        self,
        business_id,
        name,
        address,
        city,
        state,
        overall_star,
        review_count,
    ):
        self.business_id = business_id
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.overall_star = overall_star
        self.review_count = review_count


class TopDrink(db.Model):
    __tablename__ = "top_drinks"
    business_id = db.Column(db.String, primary_key=True)
    drink_name = db.Column(db.String, primary_key=True)
    score = db.Column(db.Float)

    def __init__(
        self,
        business_id,
        drink_name,
        score,
    ):
        self.business_id = business_id
        self.drink_name = drink_name
        self.score = score


class DrinkReviews(db.Model):
    __tablename__ = "drink_reviews"
    business_id = db.Column(db.String, primary_key=True)
    drink_name = db.Column(db.String, primary_key=True)
    date = db.Column(db.String)
    text = db.Column(db.String, primary_key=True)
    stars = db.Column(db.Integer)

    def __init__(
        self,
        business_id,
        drink_name,
        date,
        text,
        stars,
    ):
        self.business_id = business_id
        self.drink_name = drink_name
        self.date = date
        self.text = text
        self.stars = stars