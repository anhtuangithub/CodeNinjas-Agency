# Casting Agency API

## Capstone Project for Udacity's Full Stack Developer Nanodegree
Heroku Link: https://ry-fsnd-capstone.herokuapp.com

While running locally: http://localhost:5000

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

## Running the server

Before running the application locally, make the following changes in the `app.py` file in root directory:
- Replace the following import statements
  ```
    from database.models import db_drop_and_create_all, setup_db, Actor, Movie
    from auth.auth import AuthError, requires_auth
  ```
  with
  ```
    from .database.models import db_drop_and_create_all, setup_db, Actor, Movie
    from .auth.auth import AuthError, requires_auth
  ```
- Also, uncomment the line `db_drop_and_create_all()` on the initial run to setup the required tables in the database.

To run the server, execute:

```bash
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

Using the `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started
Base URL: This application can be run locally. The hosted version is at `https://ry-fsnd-capstone.herokuapp.com`.

Authentication: This application requires authentication to perform various actions. All the endpoints require
various permissions, except the root (or health) endpoint, that are passed via the `Bearer` token.

The application has three different types of roles:
- Casting Assistant
  - Can view actors and movies
  - Has `get:actors, get:actor-by-id, get:movies, get:movie-by-id` permissions
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
  - Has `post:actors, delete:actors, patch:actors, patch:movies` permissions
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database
  - Has `post:movies, delete:movies` permissions


## Error Handling

```json
{
  "success": false,
  "error": 404,
  "message": "resource not found"
}
```

```json
{
  "success": false,
  "error": 422,
  "message": "unprocessable"
}
```

```json
{
  "success": false,
  "error": 400,
  "message": "Bad request"
}
```

```json
{
  "success": false,
  "error": 405,
  "message": "Method not allowed"
}
```

```json
{
  "success": false,
  "error": 500,
  "message": "Internal server error"
}
```

The API will return the following errors based on how the request fails:
 - 400: Bad Request

## Endpoints

#### GET /
 - General
   - root endpoint
   - can also work to check if the api is up and running
   - is a public endpoint, requires no authentication
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/`

<details>
<summary>Sample Response</summary>

```
{
    "/": "Running!!"
}
```

</details>

#### GET /actors
 - General
   - gets the list of all the actors
   - requires `get:actors` permission
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/actors`

<details>
<summary>Sample Response</summary>

```
{
    "actors": [
        {
            "id": 1,
            "name": "Anne Hathaway"
        },
        {
            "id": 2,
            "name": "Matthew McConaughey"
        },
        {
            "id": 3,
            "name": "Margot Robbie"
        },
        {
            "id": 4,
            "name": "Mary Elizabeth Winstead"
        }
    ],
    "success": true
}
```

</details>

#### GET /actors/{actor_id}
 - General
   - gets the complete info for an actor
   - requires `get:actor-by-id` permission
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/actors/1`

<details>
<summary>Sample Response</summary>

```
{
    "actor": {
        "date_of_birth": "November 12, 1982",
        "full_name": "Anne Jacqueline Hathaway",
        "movies": [
            "Serenity"
        ],
        "name": "Anne Hathaway"
    },
    "success": true
}
```
  
</details>

#### POST /actors
 - General
   - creates a new actor
   - requires `post:actors` permission
 
 - Request Body
   - name: string, required
   - full_name: string, optional
   - date_of_birth: date, required
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/actors`
   - Request Body
     ```
        {
            "name": "Ana de Armas",
            "full_name": "Ana Celia de Armas Caso",
            "date_of_birth": "April 30, 1988"
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "created_actor_id": 5,
    "success": true
}
```
  
</details>

#### PATCH /actors/{actor_id}
 - General
   - updates the info for an actor
   - requires `patch:actors` permission
 
 - Request Body (at least one of the following fields required)
   - name: string, optional
   - full_name: string, optional
   - date_of_birth: date, optional
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/actors/5`
   - Request Body
     ```
       {
            "full_name": "Ana de Arams Caso"
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "actor_info": {
        "date_of_birth": "April 30, 1988",
        "full_name": "Ana de Arams Caso",
        "name": "Ana de Armas"
    },
    "success": true
}
```
  
</details>

#### DELETE /actors/{actor_id}
 - General
   - deletes the actor
   - requires `delete:actors` permission
   - will also delete the mapping to the movie but will not delete the movie from the database
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/actors/5`

<details>
<summary>Sample Response</summary>

```
{
    "deleted_actor_id": 5,
    "success": true
}
```
  
</details>

#### GET /movies
 - General
   - gets the list of all the movies
   - requires `get:movies` permission
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/movies`

<details>
<summary>Sample Response</summary>

```
{
    "movies": [
        {
            "id": 1,
            "release_year": 2019,
            "title": "Serenity"
        },
        {
            "id": 2,
            "release_year": 2020,
            "title": "Birds of Prey"
        }
    ],
    "success": true
}
```

</details>

#### GET /movies/{movie_id}
 - General
   - gets the complete info for a movie
   - requires `get:movie-by-id` permission
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/movies/1`

<details>
<summary>Sample Response</summary>

```
{
    "movie": {
        "cast": [
            "Anne Hathaway",
            "Matthew McConaughey"
        ],
        "duration": 106,
        "imdb_rating": 5.3,
        "release_year": 2019,
        "title": "Serenity"
    },
    "success": true
}
```
  
</details>

#### POST /movies
 - General
   - creates a new movie
   - requires `post:movies` permission
 
 - Request Body
   - title: string, required
   - duration: integer, required
   - release_year: integer, required
   - imdb_rating: float, required
   - cast: array of string, non-empty, required
 
 - NOTE
   - Actors passed in the `cast` array in request body must already exist in the database prior to making this request.
   - If not, the request will fail with code 422.
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/actors`
   - Request Body
     ```
        {
            "title": "Knives Out",
            "duration": 130,
            "release_year": 2019,
            "imdb_rating": 7.9,
            "cast": ["Ana de Armas"]
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "created_movie_id": 3,
    "success": true
}
```
  
</details>

#### PATCH /movie/{movie_id}
 - General
   - updates the info for a movie
   - requires `patch:movies` permission
 
 - Request Body (at least one of the following fields required)
   - title: string, optional
   - duration: integer, optional
   - release_year: integer, optional
   - imdb_rating: float, optional
   - cast: array of string, non-empty, optional
 
 - NOTE
   - Actors passed in the `cast` array in request body will completely replace the existing relationship.
   - So, if you want to append new actors to a movie, pass the existing actors also in the request.
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/movies/3`
   - Request Body
     ```
       {
            "imdb_rating": 8.1
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "movie_info": {
        "duration": 130,
        "imdb_rating": 8.1,
        "release_year": 2019,
        "title": "Knives Out"
    },
    "success": true
}
```
  
</details>

#### DELETE /movies/{movie_id}
 - General
   - deletes the movie
   - requires `delete:movies` permission
   - will not affect the actors present in the database
 
 - Sample Request
   - `https://render-deployment-example-nuov.onrender.com/movies/3`

<details>
<summary>Sample Response</summary>

```
{
    "deleted_movie_id": 3,
    "success": true
}
```
  
</details>

## Testing
For testing the backend, run the following commands (in the exact order):
```
dropdb capstone_test
createdb capstone_test
psql capstone_test < casting.sql
python test.py
```

Alternate way: Create the db `capstone_test` using PgAdmin and copy the contents of casting.sql and paste them
in Query tool in PgAdmin and create the db table with records. Then, run the command `python test.py`.# CodeNinjas-Agency
# CodeNinjas-Agency
