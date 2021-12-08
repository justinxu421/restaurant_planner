"""
app 
"""

from typing import List

from flask import Flask
from flask_migrate import Migrate

from boba_business import BobaBusiness
from models import Business, DrinkReviews, TopDrink, db

db_name = "boba_data.db"
app = Flask(__name__)
migrate = Migrate()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)
migrate.init_app(app, db)


def force_load_top_drinks(name: str, num_drinks=10):
    bb = BobaBusiness(name)
    business_item = Business(
        bb.bid, bb.name, bb.address, bb.city, bb.state, bb.overall_star, bb.review_count
    )
    db.session.add(business_item)
    top_drinks = bb.get_drink_items()

    # drop existing reviews and drinks to prevent double writing
    TopDrink.query.filter_by(business_id=bb.bid).delete()
    DrinkReviews.query.filter_by(business_id=bb.bid).delete()
    db.session.commit()

    for drink in top_drinks:
        drink_item = TopDrink(bb.bid, drink["drink_name"], drink["score"])
        db.session.add(drink_item)
        for review in drink["reviews"]:
            review_item = DrinkReviews(
                bb.bid,
                drink["drink_name"],
                review["date"],
                review["text"],
                review["stars"],
            )
            db.session.add(review_item)
    db.session.commit()

    return {
        "business_name": bb.name,
        "business_id": bb.bid,
        "address": bb.address,
        "city": bb.city,
        "state": bb.state,
        "overall_stars": bb.overall_star,
        "top_drinks": top_drinks[:num_drinks],
    }


def serialize_reviews(reviews):
    return [
        {
            "stars": review.stars,
            "text": review.text,
            "date": review.date,
        }
        for review in reviews
    ]


def get_drink_payload(business: Business, drinks: List[DrinkReviews], num_drinks=10):
    top_drinks = []
    for drink in drinks[:num_drinks]:
        reviews = DrinkReviews.query.filter_by(
            business_id=business.business_id, drink_name=drink.drink_name
        ).all()
        drink_info = {
            "drink_name": drink.drink_name,
            "score": drink.score,
            "reviews": serialize_reviews(reviews),
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


@app.route("/business/<name>")
def get_top_drinks(name: str):
    # if it exists in the database, read and return
    business = Business.query.filter_by(name=name).first()
    if business:
        # check if drinks are saved
        drinks = (
            TopDrink.query.filter_by(business_id=business.business_id)
            .order_by(TopDrink.score.desc())
            .all()
        )
        print(drinks)
        if drinks:
            return get_drink_payload(business, drinks)

    # otherwise we need to call our NLP API and then save our info
    return force_load_top_drinks(name)


@app.route("/force/business/<name>")
def force_get_top_drinks(name: str):
    # force call the NLP API to return info
    return force_load_top_drinks(name)


@app.route("/")
def hello():
    return "<h1> Hello World </h1>"
