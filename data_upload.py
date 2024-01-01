from models import Author, Quote
from connection_code import connect
import json

connect

quotes_file = r"quotes.json"
authors_file = r"authors.json"

with open(authors_file, "r") as fh:
    unpacked_authors = json.load(fh)

with open(quotes_file, "r") as fh:
    unpacked_quotes = json.load(fh)

authors_instances = [Author(**author) for author in unpacked_authors]

for author in authors_instances:
    aut = author
    aut.save()

quotes_instances = [
    Quote(
        tags=quote.get("tags", []),
        author=Author.objects(fullname=quote.get("author")).first(),
        quote=quote.get("quote", ""),
    )
    for quote in unpacked_quotes
]

for quote in quotes_instances:
    quote.save()
