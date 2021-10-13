import pandas as pd
import numpy as np
import ast
from functools import partial

CAMBRIDGE = (42.3736, -71.1097)

def get_distance_in_miles_to_point(row, center = CAMBRIDGE):
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
    """Process a df to make categories column as list
    """
    df.categories = df.categories.apply(lambda x: x.split(',') if x else x)
    return df
    
def process_df_dicts(df):
    """Process a df to make relevant columns formatted as dictionaries
    """
    df.attributes = df.attributes.apply(lambda x: ast.literal_eval(x) if x else x)
    df.hours = df.hours.apply(lambda x: ast.literal_eval(x) if x else x)
    return df
    
def get_businesses_within_distance(df_business, center_coords, center_name, radius, save = False):
    """Filter a dataframe so that businesses within a certain radius (in miles) of center are included
    """
    gdimtp = partial(get_distance_in_miles_to_point, center = center_coords)
    df_business['distance_to_cambridge'] = df_business.apply(gdimtp, axis=1)
    df_close = df_business[df_business.distance_to_cambridge <= radius]
    if save:
        df_close.to_csv(f'data/businesses_within_{radius}_miles_of_{center_name}.csv', index=False)
    return df_close

def filter_df_with_categories(df, category_filter):
    """Filter the dataframe to businesses that have at least one occurrence of the category filter
    """
    return df[df.categories.apply(lambda x: category_filter in x)] 

def load_close_businesses_and_process_and_save(center_coords, center_name, radius):
    """Read in yelp business dataset and find the rows of within radius (in miles) of center
    """
    from os.path import exists
    file_name = f'data/businesses_within_{radius}_miles_of_{center_name}.csv'
    if exists(file_name):
        df_close = pd.read_csv(file_name, keep_default_na = False)
        df_close = process_df_dicts(df_close)
    else:
        df_business = pd.read_json('yelp_dataset/yelp_academic_dataset_business.json', lines=True)
        df_close = get_businesses_within_distance(df_business, center_coords, center_name, radius, save = True)
    return process_df_categories(df_close)