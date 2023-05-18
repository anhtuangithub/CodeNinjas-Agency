import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Actor, Movie
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.assistant_token = os.environ.get('assistant_token')
        self.director_token = os.environ.get('director_token')
        self.producer_token = os.environ.get('producer_token')
        self.app = create_app()
        self.client = self.app.test_client
        # setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Ana de Armas",
            "full_name": "Ana Celia de Armas Caso",
            "date_of_birth": "April 30, 1988"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Ana de Armas"
        }

        self.VALID_UPDATE_ACTOR = {
            "full_name": "Anne Hathaway"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Suicide Squad",
            "duration": 137,
            "release_year": 2016,
            "imdb_rating": 6,
            "cast": ["Margot Robbie"]
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Knives Out",
            "imdb_rating": 7.9,
            "cast": ["Ana de Armas"]
        }

        self.VALID_UPDATE_MOVIE = {
            "imdb_rating": 6.5
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)
        #     # create all tables
        #     self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_index(self):
        """Test for GET / """
        res = self.client().get('/')
        self.assertEqual(res.status_code, 200)

    def test_api_call_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/actors')

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])

    def test_get_actors_assistant(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(len(data))
        self.assertIn('actors', data)
        self.assertIsNotNone(data["actors"])

    def test_get_actors_by_id_assistant(self):
        """Passing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)
        self.assertTrue(len(data["actor"]["movies"]))
        self.assertIn('name', data['actor'])

    def test_404_get_actors_by_id_assistant(self):
        """Failing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_actor_with_assistant_token(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        }, json=self.VALID_NEW_ACTOR)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
    
    def test_get_movies_assistant(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id_assistant(self):
        """Passing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertIn('imdb_rating', data['movie'])
        self.assertIn('duration', data['movie'])
        self.assertIn('cast', data['movie'])
        self.assertTrue(len(data["movie"]["cast"]))

    def test_404_get_movie_by_id_assistant(self):
        """Failing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_movie_with_assistant_token(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.assistant_token)
        }, json=self.VALID_NEW_MOVIE)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
    # End assistant

    # Start director
    def test_create_actor_director(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_NEW_ACTOR)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created_actor_id', data)

    def test_422_create_actor_director(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_NEW_ACTOR)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_update_actor_info_director(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_UPDATE_ACTOR)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor_info', data)
        self.assertEqual(data["actor_info"]["full_name"],
                         self.VALID_UPDATE_ACTOR["full_name"])

    def test_422_update_actor_info_director(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_UPDATE_ACTOR)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_actor_with_director_token(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/3', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })
    
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
    
    def test_create_movie_director(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_NEW_MOVIE)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('created_movie_id', data)

    def test_422_create_movie_director(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_NEW_MOVIE)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_info_director(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.VALID_UPDATE_MOVIE)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie_info', data)
        self.assertEqual(data["movie_info"]["imdb_rating"],
                         self.VALID_UPDATE_MOVIE["imdb_rating"])

    def test_422_update_movie_info_director(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        }, json=self.INVALID_UPDATE_MOVIE)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_director_token(self):
        """Failing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.director_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])

    # End director

    # Start producer
    def test_delete_actor_producer(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/3', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_404_delete_actor_producer(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/9999', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_movie_producer(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })
        
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('deleted_movie_id', data)

    def test_404_delete_movie_producer(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/9999', headers={
            'Authorization': "Bearer {}".format(self.producer_token)
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    # End producer

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
