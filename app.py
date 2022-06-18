from flask import Flask, request, jsonify
from books_db_utils import search_books

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route("/books/")
def books():
    search_term = request.args.get("search")
    book_data = search_books(search_term)
    return jsonify(book_data)
