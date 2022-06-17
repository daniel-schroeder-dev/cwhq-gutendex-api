from pathlib import Path


def strip_tags(line, start_tag, end_tag):
    return line.replace(start_tag, "").replace(end_tag, "").strip()


gutendex_path = Path("../gutendex/cache/epub")


for path in gutendex_path.iterdir():
    # if path.is_dir() and path.stem.isdigit():
    if path.is_dir() and path.stem == "29019":
        book_data = {}
        book_data["id"] = int(path.stem)
        book_data["authors"] = []
        for rdf_path in path.glob("**/*.rdf"):
            lines = []
            with open(rdf_path, mode="rt", encoding="utf-8") as book_file:
                lines = book_file.readlines()
            for line in lines:
                if "<dcterms:title>" in line:
                    book_data["title"] = strip_tags(
                        line, "<dcterms:title>", "</dcterms:title>"
                    )

                if "<dcterms:creator>" in line:
                    author_data = {}

                if "</dcterms:creator>" in line:
                    book_data["authors"].append(author_data)

                if "<pgterms:name>" in line:
                    author_data["name"] = strip_tags(
                        line, "<pgterms:name>", "</pgterms:name>"
                    )

                if (
                    '<pgterms:deathdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                ):
                    author_data["death_date"] = int(
                        strip_tags(
                            line,
                            '<pgterms:deathdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                            "</pgterms:deathdate>",
                        )
                    )

                if (
                    '<pgterms:birthdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">'
                    in line
                ):
                    author_data["birth_date"] = int(
                        strip_tags(
                            line,
                            '<pgterms:birthdate rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">',
                            "</pgterms:birthdate>",
                        )
                    )

            print(book_data)
