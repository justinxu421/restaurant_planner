from flask import Flask, render_template
from boba_business import BobaBusiness

app = Flask(__name__)


@app.route("/")
def home():
    return "<p>Home</p>"


@app.route("/business/<name>")
def get_business(name):
    bb = BobaBusiness(name)
    drink_items, drink_reviews = bb.get_drink_items()
    print(drink_items)
    item_list = [item[0] for item in drink_items[:10]]
    print(item_list)
    return render_template(
        "business.html", name=name, item_list=item_list, reviews=drink_reviews
    )


if __name__ == "__main__":
    app.run(debug=True)
