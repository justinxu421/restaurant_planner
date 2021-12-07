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
            "drink_name": drink,
            "reviews": [
                {
                    "stars": review["stars"],
                    "text": review["text"],
                }
                for review in drink_reviews[drink]
            ],
        }
        for drink, _ in drink_items[:10]
    ]
    print(drinks[0])
    return {
        "drinks": drinks,
    }
