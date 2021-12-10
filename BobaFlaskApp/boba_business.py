import os
from collections import Counter, defaultdict

import pandas as pd
import spacy
from sqlalchemy import create_engine
from wordfreq import word_frequency

from constants import NOUNS_TO_EXCLUDE
from scripts import get_boba_query


def process_text(text):
    return (
        text.replace("\n", "")
        .replace('"', "")
        .replace(',', "")
        .strip()
        .lower()
        .removeprefix("the ")
        .removeprefix("my ")
        .removeprefix("real ")
        .removeprefix("their ")
        .removeprefix("amazing ")
        .removeprefix("best ")
        .removeprefix("very ")
        .removesuffix("s")
        .strip()
    )


class BobaBusiness:
    def __init__(self, name):
        self.nlp = spacy.load("en_core_web_sm")
        self.get_business_df(name)
        self.get_nouns(NOUNS_TO_EXCLUDE)

    def get_business_df(self, business_id):
        """get the first business with matching name"""
        # Read from the yelp db to get the boba dataframe
        engine = create_engine("sqlite:///../yelp.db", echo=False)
        df_filtered = pd.read_sql(
            get_boba_query(business_id),
            con=engine,
        )

        assert len(df_filtered) > 0, "No boba business found with name"
        self.name = df_filtered.iloc[0]["name"] 
        self.bid = df_filtered.iloc[0]["business_id"]
        self.df_business = df_filtered[df_filtered["business_id"] == self.bid]
        self.overall_star = self.df_business.iloc[0]["overall_star"]
        self.city = self.df_business.iloc[0]["city"]
        self.state = self.df_business.iloc[0]["state"]
        self.address = self.df_business.iloc[0]["address"]
        self.review_count = self.df_business.iloc[0]["address"]

    def get_nouns(self, to_exclude: set):
        """
        Store the noun roots in self.noun_dict_list:
            { noun_root : { noun_full_text : count } }
        Store the noun counts in self.noun_counts:
            { noun_root : count }
        Store weighted scores in self.weighted_noun_scores:
            { noun_root: weighted_score }
        """
        self.noun_dict_list = defaultdict(Counter)
        self.noun_counts = Counter()
        for text in self.df_business.text:
            doc = self.nlp(text)
            for chunk in doc.noun_chunks:
                root_text = process_text(chunk.root.text)
                full_text = process_text(chunk.text)
                if full_text not in to_exclude:
                    self.noun_dict_list[root_text][full_text] += 1
                    self.noun_counts.update([root_text])

        self.weighted_noun_scores = Counter()
        for noun, count in self.noun_counts.items():
            word_freq = word_frequency(
                self.noun_dict_list[noun].most_common(1)[0][0], "en"
            )
            score = count / word_freq if word_freq != 0 else count
            self.weighted_noun_scores[noun] = score

    def get_keyword_items(self, keywords):
        """
        get the noun chunks with corresponding noun roots of keywords and the dataframe of their reviews
        """
        items = Counter()
        for keyword in keywords:
            items += self.noun_dict_list[keyword]

        reviews_dict = {}
        for item in items:
            df = self.df_business.loc[
                self.df_business.apply(lambda x: item in process_text(x.text), 1),
                ['stars', 'text', 'date', 'review_id']
            ]
            reviews_dict[item] = df
        return items.most_common(), reviews_dict

    def serialize(self, items, reviews):
        return [
            {
                "drink_name": name,
                "score": score,
                "reviews": [
                    {
                        "stars": review["stars"],
                        "text": review["text"],
                        "date": review["date"],
                        "review_id": review["review_id"],
                    }
                    for (_, review) in reviews[name].iterrows()
                ],
            }
            for name, score in items
        ]


    def get_drink_items(self):
        drink_items, drink_reviews = self.get_keyword_items(["tea", "teas", "slush"])
        return self.serialize(drink_items, drink_reviews)

    def get_topping_items(self):
        return self.get_keyword_items(
            ["boba", "jelly", "taro"]
        )
