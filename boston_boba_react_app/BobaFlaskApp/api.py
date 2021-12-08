"""
app 
"""

from flask import Flask
from flask_migrate import Migrate
from boba_business import BobaBusiness
from models import db, BostonBobaBusiness, TopDrink, DrinkReviews
from typing import List

db_name = "boba_data.db"
app = Flask(__name__)
migrate = Migrate()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)
migrate.init_app(app, db)


def force_load(name):
    bb = BobaBusiness(name, db_name)
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
        "top_drinks": top_drinks[:10],
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


def get_payload(business: BostonBobaBusiness, drinks: List[DrinkReviews]):
    print(drinks[:10])
    top_drinks = []
    for drink in drinks[:10]:
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
def get_top_drinks(name):
    # if it exists in the database, read and return
    business = BostonBobaBusiness.query.filter_by(name=name).first()
    if business:
        # check if drinks are saved
        drinks = (
            TopDrink.query.filter_by(business_id=business.business_id)
            .order_by(TopDrink.score.desc())
            .all()
        )
        print(drinks)
        if drinks:
            return get_payload(business, drinks)

    # otherwise we need to call our NLP API and then save our info
    return force_load(name)


@app.route("/force/business/<name>")
def force_get_top_drinks(name):
    # force call the NLP API to return info
    return force_load(name)
