from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from app.db.base import Base


class Business(Base):
    __tablename__ = "businesses"
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


class BaseReviews(Base):
    __tablename__ = "reviews"
    review_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, primary_key=True)
    business_id = Column(String, primary_key=True)
    stars = Column(Integer)
    useful = Column(Integer)
    funny = Column(Integer)
    cool = Column(Integer)
    text = Column(String)
    date = Column(String)
    text_length = Column(Integer)
