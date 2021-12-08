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


class TopDrink(db.Model):
    __tablename__ = "top_drinks"
    business_id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    overall_star = db.Column(db.Float)
    review_count = db.Column(db.Integer)
    drink_count = db.Column(db.Integer)

    def __init__(
        self,
        drink_name,
        business_id,
        name,
        address,
        city,
        state,
        overall_star,
        review_count,
        drink_count,
    ):
        business_id = db.Column(db.Integer, primary_key=True)
        drink_name = db.Column(db.String, primary_key=True)
        name = db.Column(db.String)
        address = db.Column(db.String)
        city = db.Column(db.String)
        state = db.Column(db.String)
        overall_star = db.Column(db.Float)
        review_count = db.Column(db.Integer)
        drink_count = db.Column(db.Integer)


@app.route("/db/<name>")
def index(name):
    try:
        drinks = TopDrink.query.filter_by(name=name).all()
        return {drink.drink_name: drink.drink_count for drink in drinks}
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = "<h1>Something is broken.</h1>"
        return hed + error_text


@app.route("/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/business/<name>")
def get_business(name):
    bb = BobaBusiness(name)
    drink_items, drink_reviews = bb.get_drink_items()
    drinks = [
        {
            "drink_name": drink_name,
            "count": count,
            "reviews": [
                {
                    "stars": review["stars"],
                    "text": review["text"],
                }
                for review in drink_reviews[drink_name]
            ],
        }
        for drink_name, count in drink_items
    ]
    return {
        "top_drinks": drinks,
        "business_name": bb.name,
        "business_id": bb.bid,
        "address": bb.address,
        "city": bb.city,
        "state": bb.state,
        "overall_stars": bb.overall_stars,
    }
