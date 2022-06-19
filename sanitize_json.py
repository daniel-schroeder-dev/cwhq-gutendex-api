from json import load, dump

def has_dirty_title(title):
    bad_words = [
        "shit",
        "piss",
        "fuck",
        "cunt",
        "cocksucker",
        "motherfucker",
        "pussy",
        "twat",
        "tits",
        "vagina",
        "labia",
    ]
    for token in title.split(" "):
        if token.lower() in bad_words:
            print("Discarding: ", title)
            return True
    return False
    



with open("books.json", mode="rt", encoding="utf-8") as json_file:
    books = load(json_file)


print("Num books before sanitizing: ", len(books))

safe_books = []
for book in books:
    if has_dirty_title(book["title"]):
        continue
    
    safe_books.append(book)


print("Num books after sanitizing: ", len(safe_books))

with open("books.json", mode="wt", encoding="utf-8") as json_file:
    dump(safe_books, json_file)
