from src.data.database import Redisearch
from src.schemas.schema import Movie
from src.services.service import delete

if __name__ == "__main__":
    redisearch = Redisearch("idx:test")

    # Delete item with ID 100
    delete(100)

    # Check if the item was deleted
    result = redisearch.get_item(100)
    print(f"Retrieved movie with ID {100}: {result}")
