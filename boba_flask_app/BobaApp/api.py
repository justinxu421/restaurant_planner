"""
app 
"""

from flask import Flask
from boba_business import BobaBusiness
from models import db, BostonBobaBusiness, TopDrink, DrinkReviews

db_name = "yelp.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_name
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)


@app.route("/business/<name>")
def get_top_drinks(name):
    # if it exists in the database, read and return
    business = BostonBobaBusiness.query.filter_by(name=name).first()
    print(business)
    if business:
        print(business.business_id)
        drinks = (
            TopDrink.query.filter_by(business_id=business.business_id)
            .order_by(TopDrink.score)
            .all()
        )
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
                        "reviews": [
                            {
                                "stars": review.stars,
                                "text": review.text,
                                "date": review.date,
                            }
                            for review in reviews
                        ],
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

    # otherwise we need to call our NLP API and then save our info
    bb = BobaBusiness(name)
    top_drinks = bb.get_drink_items()
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
