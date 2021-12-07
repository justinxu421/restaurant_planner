from wordfreq import word_frequency
from collections import defaultdict, Counter
import spacy
import pandas as pd


def process_text(text):
    return text.strip().lower().replace("\n", " ")


class BobaBusiness:
    def __init__(self, name):
        # TODO: load from db, for now load from csv
        self.nlp = spacy.load("en_core_web_sm")
        self.get_business_df(name)
        self.get_nouns()

    def get_business_df(self, name):
        """get the first business with matching name"""
        df = pd.read_csv("data/boston_boba_reviews.csv")
        df_filtered = df[df["name"] == name]
        assert len(df_filtered) > 0, "No boba business found with name"
        bid = df_filtered.iloc[0]["business_id"]
        self.df_business = df[df["business_id"] == bid]

    def get_nouns(self):
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
        '''
        get the noun chunks with corresponding noun roots of keywords and the dataframe of their reviews
        '''
        items = Counter()
        for keyword in keywords:
            items += self.noun_dict_list[keyword]
        reviews_dict = {}
        for item in items:
            df = self.df_business[self.df_business.apply(lambda x: item in process_text(x.text), 1)]
            reviews_dict[item] = df.to_dict('records')
        return items.most_common(), reviews_dict

    def get_drink_items(self):
        drink_items, drink_reviews = self.get_keyword_items(['tea', 'teas', 'slush'])
        return drink_items, drink_reviews

    def get_topping_items(self):
        topping_items, topping_reviews =  self.get_keyword_items(['boba', 'jelly', 'taro'])
        return topping_items, topping_reviews
