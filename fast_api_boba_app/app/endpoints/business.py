from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import dependencies
from app.models.business import Business, TopDrink, DrinkReviews
from ml_model.boba_business import BobaBusiness

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


@router.get("/home")
def get_all_business(db: Session = Depends(dependencies.get_db)):
    businesses = db.query(Business).order_by(Business.business_id).limit(10).all()
    return {"businesses": [get_business_info(x) for x in businesses]}


@router.get("/{business_id}/info")
def get_business(*, db: Session = Depends(dependencies.get_db), business_id: str):
    business = db.query(Business).filter_by(business_id=business_id).first()
    if business:
        return get_business_info(business)
    else:
        raise HTTPException(status_code=400, detail="Business does not exist")


def force_load_top_drinks(db: Session, business_id: str, num_drinks=10):
    bb = BobaBusiness(business_id)
    print('boba business')
    print(bb.bid)

    # drop existing business reviews and drinks to prevent double writing
    db.query(TopDrink).filter_by(business_id=business_id).delete()
    db.query(DrinkReviews).filter_by(business_id=business_id).delete()
    db.commit()

    top_drinks = bb.get_drink_items()
    print(top_drinks)

    for drink in top_drinks:
        drink_item = TopDrink(
            business_id=business_id,
            drink_name=drink["drink_name"],
            score=drink["score"],
        )
        db.add(drink_item)
        for review in drink["reviews"]:
            review_item = DrinkReviews(
                business_id=business_id,
                drink_name=drink["drink_name"],
                review_id=review["review_id"],
                date=review["date"],
                text=review["text"],
                stars=review["stars"],
            )
            db.add(review_item)
    db.commit()

    return {
        "top_drinks": top_drinks[:num_drinks],
    }


def serialize_reviews(reviews: DrinkReviews):
    return [
        {
            "stars": review.stars,
            "text": review.text,
            "date": review.date,
        }
        for review in reviews
    ]


def get_drink_payload(db: Session, business_id: str, drinks: List[DrinkReviews], num_drinks=10):
    top_drinks = []
    for drink in drinks[:num_drinks]:
        reviews = db.query(DrinkReviews).filter_by(
            business_id=business_id, drink_name=drink.drink_name
        ).all()
        drink_info = {
            "drink_name": drink.drink_name,
            "score": drink.score,
            "reviews": serialize_reviews(reviews),
        }
        top_drinks.append(drink_info)

    return {
        "top_drinks": top_drinks,
    }


@router.get("/{business_id}/top_drinks")
def get_top_drinks(business_id: str, db: Session = Depends(dependencies.get_db)):
    # if it exists in the database, read and return
    drinks = (
        db.query(TopDrink)
        .filter_by(business_id=business_id)
        .order_by(TopDrink.score.desc())
        .all()
    )
    print(drinks)
    if drinks:
        return get_drink_payload(db, business_id, drinks)

    # otherwise we need to call our NLP API and then save our info
    return force_load_top_drinks(db, business_id)


@router.get("/{business_id}/top_drinks/force")
def force_get_top_drinks(business_id: str, db: Session = Depends(dependencies.get_db)):
    # force call the NLP API to return info
    return force_load_top_drinks(db, business_id)
