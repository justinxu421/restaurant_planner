import pandas as pd
import numpy as np
import ast
from functools import partial
from sqlalchemy import create_engine

from constants import COORD_DICT


def get_distance_in_miles_to_point(row, center):
    """Helper function that given a dataframe row, calculates the distance
       Should likely be used within an apply function on a pandas dataframe

    Args:
        row (df): singular dataframe row
        center (Tuple[Longitude, Latitude]): the longitude/latitude of the reference point

    Returns:
        distance in miles to the point
    """
    from geopy.distance import distance

    point = (row.latitude, row.longitude)
    return distance(point, center).miles


def process_df_categories(df):
    """Process a df to make categories column as list"""
    df.categories = df.categories.apply(lambda x: x.split(",") if x else x)
    return df


def process_df_dicts(df):
    """Process a df to make relevant columns formatted as dictionaries"""
    df.attributes = df.attributes.apply(lambda x: ast.literal_eval(x) if x else x)
    df.hours = df.hours.apply(lambda x: ast.literal_eval(x) if x else x)
    return df


def process_df_all(df):
    """Process all dict and list columns in dataframe"""
    return process_df_dicts(process_df_categories(df))


def insert_distance_to_location_column(df_business, center_name):
    """Insert column to dataframe with the distance (in miles) to center"""
    if center_name in COORD_DICT:
        center_coords = COORD_DICT[center_name]
        distance_fun = partial(get_distance_in_miles_to_point, center=center_coords)
        center_distance_colname = f"distance_to_{center_name}"
        df_business[center_distance_colname] = df_business.apply(distance_fun, axis=1)
        return df_business
    else:
        print(f"{center_name} is not found, returning original dataframe")
        return df_business


def insert_text_length_column(df):
    """Insert a column to dataframe with length of text"""
    print("writing text length column")
    df["text_length"] = df.text.apply(lambda x: x.count(" "))
    return df


def insert_sentiment_column(df):
    """insert a column to dataframe with polarity and subjectivity sentiment"""
    from textblob import TextBlob

    print("writing sentiment columns")
    df["polarity"], df["subjectivity"] = zip(
        *df.text.apply(lambda x: TextBlob(x).sentiment)
    )
    return df


def filter_df_with_categories(df, category_filter):
    """Filter the dataframe to businesses that have at least one occurrence of the category filter"""
    return df[df.categories.apply(lambda x: category_filter in x)]


def get_join_query(table, center_name, radius):
    return f"""
            SELECT 
                b.business_id,
                name,
                address,
                city,
                state,
                b.stars,
                distance_to_{center_name},
                attributes,
                categories,
                hours,
                text,
                text_length,
                polarity,
                subjectivity
            FROM businesses as b
            LEFT JOIN {table} 
                ON b.business_id = {table}.business_id
            WHERE distance_to_{center_name} <= {radius}
            """


def load_close_tips(center_name, radius):
    """Read in yelp tips dataset and join with corresponding close businesses dataset"""
    engine = create_engine("sqlite:///yelp.db", echo=False)
    query = get_join_query("tips", center_name, radius)
    print(query)
    df_close_tips = pd.read_sql(
        query,
        con=engine,
    )
    return process_df_all(df_close_tips)


def load_close_reviews(center_name, radius):
    """Read in yelp tips dataset and join with corresponding close businesses dataset"""
    engine = create_engine("sqlite:///yelp.db", echo=False)
    query = get_join_query("reviews", center_name, radius)
    print(query)
    df_close_reviews = pd.read_sql(
        query,
        con=engine,
    )
    return process_df_all(df_close_reviews)


def load_close_businesses(center_name, radius):
    """Read in yelp business dataset and find the rows of within radius (in miles) of center"""
    engine = create_engine("sqlite:///yelp.db", echo=False)
    query = f"SELECT * FROM businesses WHERE distance_to_{center_name} <= {radius}"
    print(query)
    df_close = pd.read_sql(
        query,
        con=engine,
    )
    return process_df_all(df_close)
