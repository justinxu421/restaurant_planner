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


def force_load_top_drinks(business_id: str, num_drinks=10):
    bb = BobaBusiness(business_id)

    # drop existing business reviews and drinks to prevent double writing
    Business.query.filter_by(business_id=business_id).delete()
    TopDrink.query.filter_by(business_id=business_id).delete()
    DrinkReviews.query.filter_by(business_id=business_id).delete()
    db.session.commit()

    business_item = Business(
        business_id,
        bb.name,
        bb.address,
        bb.city,
        bb.state,
        bb.overall_star,
        bb.review_count,
    )
    db.session.add(business_item)
    top_drinks = bb.get_drink_items()
    print(top_drinks)

    for drink in top_drinks:
        drink_item = TopDrink(business_id, drink["drink_name"], drink["score"])
        db.session.add(drink_item)
        for review in drink["reviews"]:
            review_item = DrinkReviews(
                business_id,
                drink["drink_name"],
                review["review_id"],
                review["date"],
                review["text"],
                review["stars"],
            )
            db.session.add(review_item)
    db.session.commit()

    return {
        "business_name": bb.name,
        "business_id": business_id,
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


@app.route("/business/top_drinks/<business_id>")
def get_top_drinks(business_id: str):
    # if it exists in the database, read and return
    business = Business.query.filter_by(business_id=business_id).first()
    if business:
        # check if drinks are saved
        drinks = (
            TopDrink.query.filter_by(business_id=business_id)
            .order_by(TopDrink.score.desc())
            .all()
        )
        print(drinks)
        if drinks:
            return get_drink_payload(business, drinks)

    # otherwise we need to call our NLP API and then save our info
    return force_load_top_drinks(business_id)


def get_business_info(business: Business):
    return {
        "business_id": business.business_id,
        "name": business.name,
        "address": business.address,
        "city": business.city,
        "state": business.state,
        "overall_star": business.overall_star,
    }


@app.route("/business/values/<business_id>")
def get_business(business_id):
    business = Business.query.filter_by(business_id=business_id).first()
    return get_business_info(business)


@app.route("/business/home")
def get_businesses():
    businesses = Business.query.order_by(Business.business_id).limit(10).all()
    return {"businesses": [get_business_info(x) for x in businesses]}


@app.route("/force/business/top_drink/<business_id>")
def force_get_top_drinks(business_id: str):
    # force call the NLP API to return info
    return force_load_top_drinks(business_id)


@app.route("/")
def hello():
    return "<h1> Hello World </h1>"
