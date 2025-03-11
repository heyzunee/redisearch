from src.data.database import Redisearch

if __name__ == "__main__":
    redisearch = Redisearch("idx:test")

    redisearch.create_index()

    # Get the list of existing indices
    indices = redisearch.get_index()
    print(f"Existing indices: {indices}")
