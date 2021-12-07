"""
app 
"""

import time
from flask import Flask, jsonify
from boba_business import BobaBusiness

app = Flask(__name__)


@app.route("/time")
def get_current_time():
    return {"time": time.time()}


@app.route("/business/<name>")
def get_business(name):
    bb = BobaBusiness(name)
    drink_items, drink_reviews = bb.get_drink_items()
    drinks = [
        {
            "drink_name": drink_name,
            "count": count,
            "reviews": [
                {
                    "stars": review["stars"],
                    "text": review["text"],
                }
                for review in drink_reviews[drink_name]
            ],
        }
        for drink_name, count in drink_items[:10]
    ]
    return {
        "top_drinks": drinks,
        "business_name": bb.name,
        "business_id": bb.bid,
        "address": bb.address,
        "city": bb.city,
        "state": bb.state,
        "overall_stars": bb.overall_stars,
    }
