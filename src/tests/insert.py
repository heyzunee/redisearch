from src.data.database import Redisearch
from src.schemas.schema import Movie
from src.services.service import insert

if __name__ == "__main__":
    redisearch = Redisearch("idx:test")

    # # Add first 100 items from the CSV file
    # redisearch.add_document()

    # # Retrieve all items
    # items = redisearch.retrieve_all_items()
    # for item in items:
    #     print(item)

    # Insert a new item
    request = Movie(
        **{
            "id": "105",
            "title": "The Curious Case of Benjamin Button",
            "director": "David Fincher",
            "genres": ["Fantasy", "Drama", "Thriller", "Mystery", "Romance"],
            "vote_average": 7.3,
        }
    )
    result = insert(request)
    print(f"Retrieved movie with ID {request.id}: {result}")
