import json

from src.data.database import Redisearch
from src.schemas.schema import Movie


def insert(request: Movie, index_name="idx:test"):
    """Inserts a new request document into the Redisearch index."""
    redisearch = Redisearch(index_name)
    try:
        # Insert the into Redis using hset
        __dict = request.dict()
        __dict["genres"] = json.dumps(__dict["genres"])
        redisearch.client.redis.hset(f"doc:{request.id}", mapping=__dict)
        print(f"Inserted request with ID: {request.id}")
        return redisearch.get_item(request.id)
    except Exception as e:
        print(f"Failed to insert request with ID: {request.id}: {str(e)}")
        return None


def delete(request_id: str, index_name="idx:test"):
    """Deletes a request document from the Redisearch index."""
    redisearch = Redisearch(index_name)
    try:
        # Delete the request document from Redisearch
        redisearch.client.delete_document(f"doc:{request_id}")
        print(f"Deleted request with ID: {request_id}")
    except Exception as e:
        print(f"Failed to delete request with ID {request_id}: {str(e)}")


def update(id, request: dict, index_name="idx:test"):
    """Updates a request document in the Redisearch index."""
    redisearch = Redisearch(index_name)
    try:
        # Get the request document from Redisearch
        item = redisearch.get_item(id)
        if not item:
            print(f"Movie with ID {id} not found.")
            return

        if "genres" in item and isinstance(item["genres"], str):
            item["genres"] = json.loads(item["genres"])

        item = Movie(**item)
        item = item.dict()

        # Update the request document in Redis using hset
        item.update(request)
        if "genres" in item:
            item["genres"] = json.dumps(item["genres"])
        redisearch.client.redis.hset(f"doc:{id}", mapping=item)
        print(f"Updated request with ID: {id}")
        return redisearch.get_item(id)
    except Exception as e:
        print(f"Failed to update request with ID: {id}: {str(e)}")


def search(search_term: str, field: str, index_name="idx:test"):
    redisearch = Redisearch(index_name)
    return redisearch.search_document(
        search_term=search_term,
        field=field,
        limit=1000,
        offset=0,
        use_sort_by=True,
        # use_aggregation=True,
    )
