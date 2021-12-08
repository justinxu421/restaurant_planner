# restaurant_planner

Run these steps :

0. Download Yelp data from https://www.yelp.com/dataset/download  and unzip so that you have a `yelp_dataset` and `yelp_photos` folder

1. Make a virtual env `pip install -r requirements.txt`

2. Install TextBlob model `python -m textblob.download_corpora`

3. Install spacy en core `python -m spacy download en_core_web_sm`

4. Initialize the sqlite database with business data, tips, and reviews `python load_yelp_data_to_sqlite.py -b -t -r`, the sqlite database will be stored in `yelp.db`
