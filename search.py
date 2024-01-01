from connection_code import connect
from models import Author, Quote
import json
import redis
from redis_lru import RedisLRU
from datetime import datetime

connect

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def search_all(k):
    start = datetime.now()
    quotes = Quote.objects()
    end = datetime.now()
    print(end - start)
    return quotes


@cache
def author_search(author_to_search):
    quotes = Quote.objects(Author.fullname == author_to_search)
    return quotes


@cache
def tag_search(tag_to_search):
    quotes = Quote.objects(tags__contains=tag_to_search)
    return quotes


def multi_tag_search(multi_tags_to_search=str):
    tags_list1 = multi_tags_to_search.split(",")
    tags_list = [
        el.strip() for el in tags_list1
    ]
    quotes = Quote.objects(tags__in=tags_list)
    return quotes


def parse_input(user_input):
    try:
        input_command = user_input.split(":")[0].strip()
        input_parameter = user_input.split(":")[1].strip()
    except IndexError as e:
        print(f"pls add command and parameter, error: {e}")

    if not input_parameter:
        print("pls add mandatory parameter")
    else:
        try:
            func = commands[input_command]
            return func(input_parameter)
        except Exception as e:
            print(f"en error occured: {e}")


commands = {
    "name": author_search,
    "tag": tag_search,
    "tags": multi_tag_search,
    "all": search_all,
}


def main():
    while True:
        user_input = input("your input: ")

        if user_input.startswith("exit"):
            print("Good bye!")
            break

        quotes = parse_input(user_input)
        try:
            quotes[0]
            for quote in quotes:
                quote_dict = quote.to_json()
                utf8_json = json.dumps(quote_dict, ensure_ascii=False).encode("utf-8")
                print(utf8_json)
        except IndexError:
            print("nothing found")


if __name__ == "__main__":
    main()
