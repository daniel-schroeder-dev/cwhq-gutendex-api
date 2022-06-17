from pathlib import Path
from json import dumps
import sqlite3

con = sqlite3.connect("books.sqlite")
cur = con.cursor()


def strip_tags(line, start_tag, end_tag):
    return line.replace(start_tag, "").replace(end_tag, "").strip()


"""
CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT UNIQUE,
    birth_year INTEGER,
    death_year INTEGER
);
"""


def insert_authors(book_data):
    author_ids = []
    for author in book_data["authors"]:
        author_name = author.get("name")
        birth_year = author.get("birth_year")
        death_year = author.get("death_year")

        query = """
            SELECT * FROM authors WHERE author_name = ?;
        """
        row = cur.execute(query, [author_name]).fetchone()
        if row is not None:
            continue

        query = """
            INSERT INTO authors (author_name, birth_year, death_year)
            VALUES (?, ?, ?);
        """
        cur.execute(query, [author_name, birth_year, death_year])
        author_ids.append(str(cur.lastrowid))
        con.commit()

    return ",".join(author_ids)


"""
CREATE TABLE translators (
    translator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    translator_name TEXT UNIQUE,
    birth_year INTEGER,
    death_year INTEGER
);
"""


def insert_translators(book_data):
    translator_ids = []
    for translator in book_data["translators"]:
        translator_name = translator.get("name")
        birth_year = translator.get("birth_year")
        death_year = translator.get("death_year")

        query = """
            SELECT * FROM translators WHERE translator_name = ?;
        """
        row = cur.execute(query, [translator_name]).fetchone()
        if row is not None:
            continue

        query = """
            INSERT INTO translators (translator_name, birth_year, death_year)
            VALUES (?, ?, ?);
        """
        cur.execute(query, [translator_name, birth_year, death_year])
        translator_ids.append(str(cur.lastrowid))
        con.commit()

    return ",".join(translator_ids)


"""
CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT UNIQUE
);
"""


def insert_subjects(book_data):
    subject_ids = []
    for subject in book_data["subjects"]:
        query = """
            SELECT * FROM subjects WHERE subject_name = ?;
        """
        row = cur.execute(query, [subject]).fetchone()
        if row is not None:
            continue

        query = """
            INSERT INTO subjects (subject_name) VALUES (?);
        """
        cur.execute(query, [subject])
        subject_ids.append(str(cur.lastrowid))
        con.commit()

    return ",".join(subject_ids)


"""
CREATE TABLE formats (
    format_id INTEGER PRIMARY KEY AUTOINCREMENT,
    format_type TEXT,
    format_link TEXT
);
"""


def insert_formats(book_data):
    format_ids = []
    for format_type, format_link in book_data["formats"].items():
        query = """
            INSERT INTO formats (format_type, format_link) VALUES (?, ?);
        """
        cur.execute(query, [format_type, format_link])
        format_ids.append(str(cur.lastrowid))
        con.commit()

    return ",".join(format_ids)


"""
CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    download_count INTEGER,
    author_ids TEXT,    -- Maybe do this as CSV? 
    translator_ids TEXT,
    subject_ids TEXT,
    format_ids TEXT
);
"""


def insert_book(book_data, author_ids, translator_ids, subject_ids, format_ids):
    query = """
        INSERT INTO books 
        (book_id, title, download_count, author_ids, translator_ids, subject_ids, format_ids)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cur.execute(
        query,
        [
            book_data.get("id"),
            book_data.get("title"),
            book_data.get("download_count"),
            author_ids,
            translator_ids,
            subject_ids,
            format_ids,
        ],
    )
    con.commit()


gutendex_path = Path("../gutendex/cache/epub")

counter = 0

for path in gutendex_path.iterdir():
    counter += 1
    print(counter)
    # if counter >= 100:
    #     break
    if path.is_dir() and path.stem.isdigit():
        # if path.is_dir() and path.stem == "29019" or path.stem == "2610":
        book_data = {}
        book_data["id"] = int(path.stem)
        book_data["authors"] = []
        book_data["translators"] = []
        book_data["subjects"] = []
        book_data["formats"] = {}

        format_url = None

        adding_authors = False
        adding_translators = False
        adding_subjects = False
        adding_formats = False

        for rdf_path in path.glob("**/*.rdf"):
            lines = []
            with open(rdf_path, mode="rt", encoding="utf-8") as book_file:
                lines = book_file.readlines()

            for line in lines:

                # Getting the title
                if "<dcterms:title>" in line:
                    book_data["title"] = strip_tags(
                        line, "<dcterms:title>", "</dcterms:title>"
                    )

                # Authors toggle
                if "<dcterms:creator>" in line:
                    author_data = {}
                    adding_authors = True

                if "</dcterms:creator>" in line:
                    book_data["authors"].append(author_data)
                    adding_authors = False

                if "<pgterms:name>" in line and adding_authors:
                    author_data["name"] = strip_tags(
                        line, "<pgterms:name>", "</pgterms:name>"
                    )

                if (
                    '<pgterms:deathdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                    and adding_authors
                ):
                    author_data["death_year"] = int(
                        strip_tags(
                            line,
                            '<pgterms:deathdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                            "</pgterms:deathdate>",
                        )
                    )

                if (
                    '<pgterms:birthdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                    and adding_authors
                ):
                    author_data["birth_year"] = int(
                        strip_tags(
                            line,
                            '<pgterms:birthdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                            "</pgterms:birthdate>",
                        )
                    )

                # Translators toggle
                if "<marcrel:trl>" in line:
                    translator_data = {}
                    adding_translators = True

                if "</marcrel:trl>" in line:
                    book_data["translators"].append(translator_data)
                    adding_translators = False

                if "<pgterms:name>" in line and adding_translators:
                    translator_data["name"] = strip_tags(
                        line, "<pgterms:name>", "</pgterms:name>"
                    )

                if (
                    '<pgterms:deathdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                    and adding_translators
                ):
                    translator_data["death_year"] = int(
                        strip_tags(
                            line,
                            '<pgterms:deathdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                            "</pgterms:deathdate>",
                        )
                    )

                if (
                    '<pgterms:birthdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                    and adding_translators
                ):
                    translator_data["birth_year"] = int(
                        strip_tags(
                            line,
                            '<pgterms:birthdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                            "</pgterms:birthdate>",
                        )
                    )

                # Subjects toggle
                if "<dcterms:subject>" in line:
                    adding_subjects = True

                if "</dcterms:subject>" in line:
                    adding_subjects = False

                if "<rdf:value>" in line and adding_subjects:
                    subject = strip_tags(line, "<rdf:value>", "</rdf:value>")
                    book_data["subjects"].append(subject)

                # Downloads
                if (
                    '<pgterms:downloads rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                ):
                    download_count = strip_tags(
                        line,
                        '<pgterms:downloads rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                        "</pgterms:downloads>",
                    )
                    book_data["download_count"] = int(download_count)

                # Formats toggle
                if "<dcterms:hasFormat>" in line:
                    adding_formats = True

                if "</dcterms:hasFormat>" in line:
                    adding_formats = False

                if "<pgterms:file rdf:about" in line and adding_formats:
                    format_url = strip_tags(line, '<pgterms:file rdf:about="', '">')

                if (
                    '<rdf:value rdf:datatype="http://purl.org/dc/terms/IMT">' in line
                    and adding_formats
                ):
                    format_type = strip_tags(
                        line,
                        '<rdf:value rdf:datatype="http://purl.org/dc/terms/IMT">',
                        "</rdf:value>",
                    )
                    book_data["formats"][format_type] = format_url

            # print(dumps(book_data, indent=4))
            author_ids = insert_authors(book_data)
            translator_ids = insert_translators(book_data)
            subject_ids = insert_subjects(book_data)
            format_ids = insert_formats(book_data)
            insert_book(book_data, author_ids, translator_ids, subject_ids, format_ids)
