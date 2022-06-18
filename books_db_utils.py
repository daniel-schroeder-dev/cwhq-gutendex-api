from db import get_db
from json import dumps
from collections import OrderedDict


    

def _query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else [dict(r) for r in rv]


def search_books(search_term):
    query = """
        SELECT * FROM books;
    """
    all_books = _query_db(query)

    query = """
        SELECT * FROM books WHERE title LIKE ?;
    """
    search_term = [f"%{search_term}%"]
    
    title_results = _query_db(query, search_term)

    filtered_results = []

    for book in all_books:
        if book not in title_results:
            filtered_results.append(book)

    query = """
        SELECT * FROM authors WHERE author_name LIKE ?;
    """

    author_results = _query_db(query, search_term)

    query = """
        SELECT * FROM subjects WHERE subject_name LIKE ?;
    """

    subject_results = _query_db(query, search_term)

    filtered_subject_results = []
    for subject_result in subject_results:
        for title_result in title_results:
            if str(subject_result["subject_id"]) in title_result["subject_ids"]:
                break
        else:
            filtered_subject_results.append(subject_result)


    final_results = []
    for book in filtered_results:
        for filtered_subject_result in filtered_subject_results:
            if str(filtered_subject_result["subject_id"]) in book["subject_ids"]:
                final_results.append(book)
    
    book_data = title_results + final_results

    final_book_data = {
        "count": len(book_data),
        "results": [],
    }
    for book in book_data:
        print(book["format_ids"])
        d = {}
        d["id"] = book["book_id"]
        d["title"] = book["title"]
        d["authors"] = [book["author_ids"]]
        d["translators"] = [book["translator_ids"]]
        d["subjects"] = [book["subject_ids"].split(",")]
        d["formats"] = {format_id: "" for format_id in book["format_ids"].split(",")}
        d["download_count"] = book["download_count"]
        final_book_data["results"].append(d)

    # print(dumps(final_book_data, indent=4))

    return final_book_data

    
