from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Business(Base):
    business_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    overall_star = Column(Float)
    review_count = Column(Integer)


class TopDrink(Base):
    __tablename__ = "top_drinks"
    business_id = Column(String, primary_key=True, index=True)
    drink_name = Column(String, primary_key=True)
    score = Column(Float)


class DrinkReviews(Base):
    __tablename__ = "drink_reviews"
    business_id = Column(String, primary_key=True, index=True)
    drink_name = Column(String, primary_key=True)
    review_id = Column(String, primary_key=True)
    date = Column(String)
    text = Column(String)
    stars = Column(Integer)