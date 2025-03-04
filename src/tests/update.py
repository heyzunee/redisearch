from src.data.database import Redisearch
from src.schemas.schema import Movie
from src.services.service import insert, update

if __name__ == "__main__":
    redisearch = Redisearch("idx:test")

    # Insert a new item
    request = Movie(
        **{
            "id": "100",
            "title": "The Curious Case of Benjamin Button",
            "director": "David Fincher",
            "genres": ["Fantasy", "Drama", "Thriller", "Mystery", "Romance"],
            "vote_average": 7.3,
        }
    )
    insert(request)

    # Get the inserted item
    result = redisearch.get_item(request.id)
    print(f"Retrieved movie with ID {request.id}: {result}")

    # Update the item
    request = {"vote_count": 1003}
    result = update(100, request)
    print(f"Retrieved movie with ID {100}: {result}")
