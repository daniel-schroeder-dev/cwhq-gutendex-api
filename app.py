from flask import Flask, request
from books_db_utils import search_books

app = Flask(__name__)


@app.route("/books/")
def books():
    search_term = request.args.get("search")
    search_books(search_term)
    return "books"
