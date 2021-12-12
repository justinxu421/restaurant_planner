from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import dependencies
from app.models.business import Business#, TopDrink, DrinkReviews

router = APIRouter(prefix="/business", tags=["business"])


def get_business_info(business: Business):
    return {
        "business_id": business.business_id,
        "name": business.name,
        "address": business.address,
        "city": business.city,
        "state": business.state,
        "overall_star": business.overall_star,
        "review_count": business.review_count,
    }


# @router.get("/{business_id}")
# def get_business(*, db: Session = Depends(dependencies.get_db), business_id):
#     business = db.query(Business).filter_by(business_id=business_id).first()
#     return get_business_info(business)

@router.get("/home")
def get_all_business(db: Session = Depends(dependencies.get_db)):
    businesses = db.query(Business).order_by(Business.business_id).limit(10).all()
    return {"businesses": [get_business_info(x) for x in businesses]}

# def force_load_top_drinks(db, business_id: str, num_drinks=10):
#     bb = BobaBusiness(business_id)
#     print(bb.bid)

#     # drop existing business reviews and drinks to prevent double writing
#     models.TopDrink.query.filter_by(business_id=business_id).delete()
#     models.DrinkReviews.query.filter_by(business_id=business_id).delete()
#     db.session.commit()

#     top_drinks = bb.get_drink_items()

#     for drink in top_drinks:
#         drink_item = TopDrink(business_id, drink["drink_name"], drink["score"])
#         db.session.add(drink_item)
#         for review in drink["reviews"]:
#             review_item = DrinkReviews(
#                 business_id,
#                 drink["drink_name"],
#                 review["review_id"],
#                 review["date"],
#                 review["text"],
#                 review["stars"],
#             )
#             db.session.add(review_item)
#     db.session.commit()

#     return {
#         "top_drinks": top_drinks[:num_drinks],
#     }


# def serialize_reviews(reviews):
#     return [
#         {
#             "stars": review.stars,
#             "text": review.text,
#             "date": review.date,
#         }
#         for review in reviews
#     ]


# def get_drink_payload(business_id, drinks: List[DrinkReviews], num_drinks=10):
#     top_drinks = []
#     for drink in drinks[:num_drinks]:
#         reviews = DrinkReviews.query.filter_by(
#             business_id=business_id, drink_name=drink.drink_name
#         ).all()
#         drink_info = {
#             "drink_name": drink.drink_name,
#             "score": drink.score,
#             "reviews": serialize_reviews(reviews),
#         }
#         top_drinks.append(drink_info)

#     return {
#         "top_drinks": top_drinks,
#     }


# @router.get("/business/<business_id>/top_drinks")
# def get_top_drinks(business_id: str):
#     # if it exists in the database, read and return
#     drinks = (
#         TopDrink.query.filter_by(business_id=business_id)
#         .order_by(TopDrink.score.desc())
#         .all()
#     )
#     print(drinks)
#     if drinks:
#         return get_drink_payload(business_id, drinks)

#     # otherwise we need to call our NLP API and then save our info
#     return force_load_top_drinks(business_id)


# @router.get("/force/business/<business_id>/top_drinks")
# def force_get_top_drinks(business_id: str):
#     # force call the NLP API to return info
#     return force_load_top_drinks(business_id)
