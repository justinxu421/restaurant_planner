import pandas as pd
import utils
from sqlalchemy import create_engine
import argparse


def load_businesses():
    print("loading businesses")
    df_business = pd.read_json(
        "yelp_dataset/yelp_academic_dataset_business.json", lines=True
    )
    cities = ["cambridge", "stanford", "vancouver"]
    for city in cities:
        print(f"imputing distances to {city}")
        df_business = utils.insert_distance_to_location_column(df_business, city)
    # cast as string to save to database
    df_business.attributes = df_business.attributes.astype(str)
    df_business.categories = df_business.categories.astype(str)
    df_business.hours = df_business.hours.astype(str)
    engine = create_engine("sqlite:///yelp.db", echo=True)
    df_business.to_sql("businesses", con=engine, if_exists="replace")


def load_tips():
    print("loading tips")
    df_tip = pd.read_json("yelp_dataset/yelp_academic_dataset_tip.json", lines=True)
    df_tip = utils.insert_text_length_column(df_tip)
    df_tip = utils.insert_sentiment_column(df_tip)
    engine = create_engine("sqlite:///yelp.db", echo=True)
    df_tip.to_sql("tips", con=engine, if_exists="replace")


def load_reviews():
    print("loading reviews")
    df_review = pd.read_json(
        "yelp_dataset/yelp_academic_dataset_review.json", lines=True
    )
    df_review = utils.insert_text_length_column(df_review)
    df_review = utils.insert_sentiment_column(df_review)
    engine = create_engine("sqlite:///yelp.db", echo=True)
    df_review.to_sql("reviews", con=engine, if_exists="replace")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-b", "--business", help="save businesses to sql database", action="store_true"
    )
    parser.add_argument(
        "-t", "--tips", help="save tips to sql database", action="store_true"
    )
    parser.add_argument(
        "-r", "--reviews", help="save reviews to sql database", action="store_true"
    )
    args = parser.parse_args()
    if args.business:
        load_businesses()
    if args.tips:
        load_tips()
    if args.reviews:
        load_reviews()
