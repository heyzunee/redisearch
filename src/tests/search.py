from src.data.database import Redisearch
from src.services.service import search

if __name__ == "__main__":
    redisearch = Redisearch("idx:test")

    res = search(search_term="Gore", field="director")

    for movie in res:
        print(movie)
