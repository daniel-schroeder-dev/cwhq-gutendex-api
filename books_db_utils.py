from db import get_db
from json import dumps


def _query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def search_books(search_term):
    query = """
        SELECT * FROM books WHERE title LIKE ? LIMIT 10;
    """
    search_term = [f"%{search_term}%"]
    for book in _query_db(query, search_term):
        print(dumps(dict(book), indent=4))