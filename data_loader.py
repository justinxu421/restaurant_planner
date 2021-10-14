import utils


class YelpDataLoader:
    def __init__(self, center_name, radius):
        self.df_close = utils.load_close_businesses(center_name, radius)
        self.df_close_tips = utils.load_close_tips(center_name, radius)
        self.df_boba = utils.filter_df_with_categories(self.df_close, "Bubble Tea")
        self.df_pizza = utils.filter_df_with_categories(self.df_close, "Pizza")
