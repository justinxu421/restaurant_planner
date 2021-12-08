"""
app 
"""

import time
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from boba_business import BobaBusiness

db_name = "yelp.db"
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


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


@app.route("/db/<name>")
def index(name):
    business = BostonBobaBusiness.query.filter_by(name=name).first()
    if business:
        drinks = TopDrink.query.filter_by(business_id=business.business_id).all()
        if len(drinks) > 0:
            return {drink.drink_name: (drink.score, business.name) for drink in drinks}


@app.route("/business/<name>")
def get_top_drinks(name):

    # if it exists in the database, read and return
    business = BostonBobaBusiness.query.filter_by(name=name).first()
    if business:
        drinks = TopDrink.query.filter_by(business_id=business.business_id).all()
        if drinks:
            top_drinks = []
            for drink in drinks[:10]:
                reviews = DrinkReviews.query.filter_by(
                    business_id=business.business_id, drink_name=drink.drink_name
                ).all()
                if reviews:
                    drink_info = {
                        "drink_name": drink.drink_name,
                        "score": drink.score,
                        "reviews": [{
                            'stars': review.stars,
                            'text': review.text,
                            'date': review.date,
                        } for review in reviews],
                    }
                    top_drinks.append(drink_info)

            return {
                "business_name": business.name,
                "business_id": business.business_id,
                "address": business.address,
                "city": business.city,
                "state": business.state,
                "overall_stars": business.overall_star,
                "top_drinks": top_drinks,
            }

    # otherwise we need to call our NLP API
    bb = BobaBusiness(name)
    return {
        "business_name": bb.name,
        "business_id": bb.bid,
        "address": bb.address,
        "city": bb.city,
        "state": bb.state,
        "overall_stars": bb.overall_star,
        "top_drinks": bb.get_drink_items()[:10],
    }
