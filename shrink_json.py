from json import load, dump
from random import randint

with open("books.json", mode="rt", encoding="utf-8") as json_file:
    books = load(json_file)


print("Num books before filtering:", len(books))



filtered_books = []
for book in books:
    if randint(1, 2) == 1:
        filtered_books.append(book)


print("Num books after filtering: ", len(filtered_books))

with open("books.json", mode="wt", encoding="utf-8") as json_file:
    dump(filtered_books, json_file)
