import pandas as pd
import utils
from sqlalchemy import create_engine

from constants import CAMBRIDGE


def load_businesses():
    print("loading businesses")
    df_business = pd.read_json(
        "yelp_dataset/yelp_academic_dataset_business.json", lines=True
    )
    cities = ["cambridge", "stanford", "vancouver"]
    for city in cities:
        print(f"imputing distances to {city}")
        df_business = utils.impute_businesses_with_location_distance(df_business, city)
    df_business.attributes = df_business.attributes.astype(str)
    df_business.categories = df_business.categories.astype(str)
    df_business.hours = df_business.hours.astype(str)
    engine = create_engine("sqlite:///yelp.db", echo=True)
    df_business.to_sql("businesses", con=engine, if_exists="replace")


def load_tips():
    print("loading tips")
    df_tip = pd.read_json("yelp_dataset/yelp_academic_dataset_tip.json", lines=True)
    engine = create_engine("sqlite:///yelp.db", echo=True)
    df_tip.to_sql("tips", con=engine, if_exists="replace")


def load_reviews():
    print("loading reviews")
    df_review = pd.read_json(
        "yelp_dataset/yelp_academic_dataset_review.json", lines=True
    )
    engine = create_engine("sqlite:///yelp.db", echo=True)
    df_review.to_sql("reviews", con=engine, if_exists="replace")


if __name__ == "__main__":
    load_businesses()
    load_tips()
    load_reviews()
