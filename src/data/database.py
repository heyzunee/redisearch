import ast
import json

import pandas as pd
import redisearch.aggregation as aggregations
from redis import Redis, ResponseError
from src.config import REDIS_HOST, REDIS_PORT
from src.schemas.schema import Movie

from redisearch import Client, IndexDefinition, NumericField, Query, TextField


class Redisearch:
    def __init__(self, index_name=None):
        self.index_name = index_name
        self.redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        self.client = Client(self.index_name)

    def create_index(self):
        """Creates an index if it doesn't already exist."""
        try:
            # Check if index exists
            self.client.info()
            print(f"Index '{self.index_name}' already exists.")
        except ResponseError:
            schema = [
                TextField("id", weight=5.0),
                TextField("title"),
                TextField("director"),
                TextField("genres"),
                NumericField("vote_average"),
            ]
            definition = IndexDefinition(prefix=["doc:"])
            try:
                self.client.create_index(schema, definition=definition)
                print(f"Index '{self.index_name}' created successfully.")
            except ResponseError as e:
                print(f"Failed to create index '{self.index_name}': {str(e)}.")

    def get_index(self):
        """Retrieves and returns the list of existing index names."""
        try:
            indices = self.redis_conn.execute_command("FT._LIST")
            return indices
        except ResponseError as e:
            print(f"Error retrieving indices: {str(e)}")

    def delete_index(self):
        """Drops the index and deletes all associated documents."""
        try:
            self.client.drop_index()
            print(f"Index '{self.index_name}' deleted successfully.")
        except ResponseError as e:
            print(f"Error deleting index '{self.index_name}': {str(e)}")

    def get_item(self, request_id):
        """Retrieves a specific item from the Redisearch index by its ID using FT.SEARCH."""
        try:
            # Construct the search query for a specific ID
            query = Query(f"@id:{request_id}")

            # Execute the FT.SEARCH command
            results = self.client.search(query)
            results = results.docs
            return results[0].__dict__ if len(results) >= 1 else None
        except ResponseError as e:
            print(f"Error retrieving item with ID '{request_id}': {str(e)}")
            return None

    def retrieve_all_items(self):
        """Retrieves all items from the Redisearch index."""
        try:
            # Use a query that matches all documents
            query = Query("*").paging(0, 1000)  # Adjust the limit if needed
            results = self.client.search(query)

            # Collect the documents into a list
            items = [doc.__dict__ for doc in results.docs]
            print(f"Retrieved {len(items)} items from index '{self.index_name}'.")
            return items
        except ResponseError as e:
            print(f"Error retrieving items from index '{self.index_name}': {str(e)}")
            return []

    def add_document(self):
        """Reads a CSV file and adds each row as a document to the Redisearch index."""
        df = pd.read_csv("./datasets/movie.csv")
        df["genres"] = df["genres"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
        df = df.iloc[:100].copy()

        for index, row in df.iterrows():
            doc_id = f"doc:{index}"

            document = Movie(id=index, **row.to_dict())

            __dict = document.dict()
            __dict["genres"] = json.dumps(__dict["genres"])
            try:
                self.client.redis.hset(doc_id, mapping=__dict)
                print(f"Document {doc_id} added successfully.")
            except Exception as e:
                print(f"Failed to add document {doc_id}: {str(e)}")

    def search_document(
        self,
        search_term: str,
        field=None,
        limit=10,
        offset=0,
        use_aggregation=False,
        use_sort_by=False,
    ):
        """Searches for documents in the Redisearch index with various options."""
        try:
            # Create base query
            query = Query(f"@{field}:{search_term}").paging(offset, limit)

            if use_sort_by:
                query = query.sort_by("vote_average", asc=False)
            if use_aggregation:
                # Aggregate request with sorting and limits
                request = (
                    aggregations.AggregateRequest("*")
                    .filter(f"@{field} > {search_term}")
                    .sort_by(aggregations.Desc(f"@{field}"))
                    .limit(offset, limit)
                    .load(f"@{field}")
                )
                results = self.client.aggregate(request)
                print(f"Found {len(results.rows)} results with {field} = '{search_term}'.")
                return results.rows

            # Execute the search query
            results = self.client.search(query)
            search_results = [doc.__dict__ for doc in results.docs]
            print(f"Found {len(search_results)} results for search term '{search_term}'.")
            return search_results

        except Exception as e:
            print(f"Error searching for '{search_term}' in index '{self.index_name}'")
            print(e)
            return []
