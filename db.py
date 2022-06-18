import sqlite3
from flask import g

DATABASE = 'books.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        con = sqlite3.connect(DATABASE)
        con.row_factory = sqlite3.Row
        db = g._database = con
    return db