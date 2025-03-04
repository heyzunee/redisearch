# Movie Search API

## Overview
This API provides endpoints to interact with a Redisearch index for managing movie data. It allows users to insert, update, delete, and search for movie documents stored in Redis.

## Requirements
- Python 3.7+
- Redis server with Redisearch module enabled
- Required dependencies (install via `pip install -r requirements.txt`)

## Endpoints

### 1. Insert a Movie
**Description:** Adds a new movie document to the Redisearch index.

- **Endpoint:** `POST /insert`
- **Request Body:**
  ```json
  {
    "id": "1",
    "title": "Inception",
    "director": "",
    "genres": ["Sci-Fi", "Thriller"],
    "overview": "",
    "vote_average": 0.0,
    "vote_count": 2
  }
  ```
- **Response:**
  ```json
  {
    "id": "1",
    "title": "Inception",
    "director": "",
    "genres": ["Sci-Fi", "Thriller"],
    "overview": "",
    "vote_average": 0.0,
    "vote_count": 2
  }
  ```

### 2. Delete a Movie
**Description:** Removes a movie document from the Redisearch index.

- **Endpoint:** `DELETE /delete/{id}`
- **Path Parameter:** `id` (string) - The ID of the movie to delete.
- **Response:**
  ```json
  {
    "message": "Deleted request with ID: 1"
  }
  ```

### 3. Update a Movie
**Description:** Updates an existing movie document in the Redisearch index.

- **Endpoint:** `PUT /update/{id}`
- **Path Parameter:** `id` (string) - The ID of the movie to update.
- **Request Body:**
  ```json
  {
    "title": "Interstellar",
    "genres": ["Sci-Fi", "Drama"],
    "release_year": 2014
  }
  ```
- **Response:**
  ```json
  {
    "id": "1",
    "title": "Interstellar",
    "genres": ["Sci-Fi", "Drama"],
    "release_year": 2014
  }
  ```

### 4. Search Movies
**Description:** Searches for movies in the Redisearch index by a specific field.

- **Endpoint:** `GET /search`
- **Query Parameters:**
  - `search_term` (string) - The term to search for.
  - `field` (string) - The field to search in (e.g., "title").
- **Example Request:**
  ```
  GET /movies/search?search_term=Inception&field=title
  ```
- **Response:**
  ```json
  {
    "success": true,
    "data": [
        {
            "id": "doc:96",
            "payload": null,
            "vote_average": "8.1",
            "vote_count": "13752",
            "director": "Christopher Nolan",
            "genres": "[\"Action\", \"Thriller\", \"Science\", \"Fiction\", \"Mystery\", \"Adventure\"]",
            "title": "Inception",
            "overview": "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life as payment for a task considered to be impossible: \"inception\", the implantation of another person's idea into a target's subconscious."
        }
    ]
  }
  ```

## Running the API
1. Start Redis with Redisearch module enabled.
2. Run the Python server (`main.py` or `app.py`).
3. Use tools like Postman or cURL to interact with the endpoints.

## Notes
- Ensure Redis is running before using the API.
- The `index_name` is set to `idx:test` by default.
- The `Movie` schema is expected to follow the provided JSON format.

## License
MIT License

