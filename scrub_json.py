from json import load, dump

with open("books.json", mode="rt", encoding="utf-8") as json_file:
    books = load(json_file)

for book in books:
    book["title"] = book["title"].replace("&#13;", "")


with open("books.json", mode="wt", encoding="utf-8") as json_file:
    dump(books, json_file)
