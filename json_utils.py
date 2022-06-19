from json import load, dumps

def search_books(search_term):
    with open("books.json", mode="rt", encoding="utf-8") as json_file:
        book_data = load(json_file)
    
    results = []
    search_term = search_term.lower()

    for book in book_data:
        if search_term in book["title"].lower():
            results.append(book)
    
        for author in book["authors"]:
            if search_term in author["name"].lower():
                results.append(book)

        if search_term in ",".join([subject.lower() for subject in book["subjects"]]):
            print("Adding search term")
            results.append(book)
    

    json_data = {
        "count": len(results),
        "results": results,
    }

    return json_data