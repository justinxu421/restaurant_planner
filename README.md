# restaurant_planner

Run these steps 

1. Make a virtual env `pip install -r requirements.txt`

2. Install TextBlob model `python -m textblob.download_corpora`

3. Install spacy en core `python -m spacy download en_core_web_sm`

4. Initialize the sqlite database with business data `python load_yelp_data_to_sql.py -b -t -r`
