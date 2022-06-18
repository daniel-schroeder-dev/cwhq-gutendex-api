import sqlite3

DATABASE = 'books_v2.sqlite'

con = sqlite3.connect(DATABASE)
con.row_factory = sqlite3.Row
cur = con.cursor()

query = """
    SELECT book_id, title FROM books WHERE title LIKE '%&#13%';
"""

for row in cur.execute(query).fetchall():
    book_id, title = row
    title = title.replace("&#13;", "")
    query = """
        UPDATE books SET title = ? WHERE book_id = ?;
    """
    cur.execute(query, [title, book_id])
    con.commit()
