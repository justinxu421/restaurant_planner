from wordfreq import word_frequency
from collections import defaultdict, Counter
import spacy
import pandas as pd
import os
from constants import NOUNS_TO_EXCLUDE


def process_text(text):
    return (
        text.replace("\n", "")
        .replace('"', "")
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

    def get_business_df(self, name):
        """get the first business with matching name"""
        self.name = name
        # TODO: load from db, for now load from csv
        package_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file = os.path.join(package_dir, "data/boston_boba_reviews.csv")
        df = pd.read_csv(csv_file)

        df_filtered = df[df["name"] == name]
        assert len(df_filtered) > 0, "No boba business found with name"
        self.bid = df_filtered.iloc[0]["business_id"]
        self.df_business = df[df["business_id"] == self.bid]
        self.overall_stars = self.df_business.iloc[0]["overall_star"]
        self.city = self.df_business.iloc[0]["city"]
        self.state = self.df_business.iloc[0]["state"]
        self.address = self.df_business.iloc[0]["address"]

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
            df = self.df_business[
                self.df_business.apply(lambda x: item in process_text(x.text), 1)
            ]
            reviews_dict[item] = df.to_dict("records")
        return items.most_common(), reviews_dict

    def get_drink_items(self):
        drink_items, drink_reviews = self.get_keyword_items(["tea", "teas", "slush"])
        return drink_items, drink_reviews

    def get_topping_items(self):
        topping_items, topping_reviews = self.get_keyword_items(
            ["boba", "jelly", "taro"]
        )
        return topping_items, topping_reviews
