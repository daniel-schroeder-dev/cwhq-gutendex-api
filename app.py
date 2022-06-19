from flask import Flask, request, jsonify
from json_utils import search_books
from urllib.request import urlopen

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

with urlopen("") as response:
    


@app.route("/books/")
def books():
    search_term = request.args.get("search")
    book_data = search_books(search_term)
    return jsonify(book_data)
