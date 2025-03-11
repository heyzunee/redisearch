# Movie Search API

## Overview
This API provides endpoints to interact with a Redisearch index for managing movie data. It allows users to insert, update, delete, and search for movie documents stored in Redis.

## Requirements
- Python 3.7+
- Redis server with Redisearch module enabled
- Required dependencies (install via `pip install -r requirements.txt`)

## Running the API
```
scripts/run.sh
```

## Endpoints

### 1. Insert a Movie
**Description:** Adds a new movie document to the Redisearch index.

- **Endpoint:** `POST /insert`
- **Request Body:**
  ```json
  {
    "id": "100",
    "title": "The Curious Case of Benjamin Button",
    "director": "David Fincher",
    "genres": ["Fantasy", "Drama", "Thriller", "Mystery", "Romance"],
    "vote_average": 7.3,
  }
  ```
- **Response:**
  ```json
  {
    "message": "Inserted request with ID: 100",
    "data": {
        "id": "doc:100",
        "payload": null,
        "title": "The Curious Case of Benjamin Button",
        "director": "David Fincher",
        "genres": "[\"Fantasy\", \"Drama\", \"Thriller\", \"Mystery\", \"Romance\"]",
        "overview": "",
        "vote_average": "7.3",
        "vote_count": "-1"
    }
  }
  ```

### 2. Delete a Movie
**Description:** Removes a movie document from the Redisearch index.

- **Endpoint:** `DELETE /delete/{id}`
- **Path Parameter:** `id` (string) - The ID of the movie to delete.
- **Example Request:**
  ```
  DELETE /delete?id=100
  ```
- **Response:**
  ```json
  {
    "message": "Deleted request with ID: 100"
  }
  ```

### 3. Update a Movie
**Description:** Updates an existing movie document in the Redisearch index.

- **Endpoint:** `PUT /update/{id}`
- **Path Parameter:** `id` (string) - The ID of the movie to update.
- **Example Request:**
  ```
  PUT /update?id=100
  ```
- **Request Body:**
  ```json
  {
    "vote_average": 8.0,
    "vote_count": 2000
  }
  ```
- **Response:**
  ```json
  {
    "message": "Updated request with ID: 100",
    "data": {
        "id": "doc:100",
        "payload": null,
        "title": "The Curious Case of Benjamin Button",
        "director": "David Fincher",
        "genres": "[\"Fantasy\", \"Drama\", \"Thriller\", \"Mystery\", \"Romance\"]",
        "overview": "",
        "vote_average": "8.0",
        "vote_count": "2000"
    }
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
  GET /search?search_term=Inception&field=title
  ```
- **Response:**
  ```json
  {
    "message": "Found 1 items for search term 'Inception'",
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
