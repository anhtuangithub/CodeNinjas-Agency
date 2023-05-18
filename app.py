from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from database.models import ActorInMovie, db_drop_and_create_all, setup_db, Actor, Movie
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    # Uncomment the following line on the initial run to setup
    # the required tables in the database
    with app.app_context():
        db_drop_and_create_all()

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return "Welcome!!", 200

    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actors(payload):
        actors_query = Actor.query.order_by(Actor.id).all()

        return jsonify({
            "success": True,
            "actors": [actor.short_info for actor in actors_query]
        }), 200

    @app.route('/actors/<int:actor_id>')
    @requires_auth("get:actor-by-id")
    def get_actor_by_id(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first()

        if actor is None:
            return abort(404)
        return jsonify({
            "success": True,
            "actor": actor.full_info
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth("post:actors")
    def create_actor(payload):
        try:
            body = request.get_json()
            new_name = body.get('name', None)
            new_date_of_birth = body.get('date_of_birth', None)
            new_full_name = body.get('full_name', None)

            if new_name == '' or new_date_of_birth == '':
                raise ValueError

            new_actor = Actor(new_name, new_full_name,
                              new_date_of_birth)
            new_actor.insert()

            return jsonify({
                "success": True,
                "created_actor_id": new_actor.id
            }), 201

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth("patch:actors")
    def update_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first()

        if actor is None:
            return abort(404)

        try:
            body = request.get_json()
            new_name = body.get('name', None)
            new_date_of_birth = body.get('date_of_birth', None)
            new_full_name = body.get('full_name', None)

            if 'date_of_birth' in body:
                if new_date_of_birth == "":
                    raise ValueError
                actor.date_of_birth = new_date_of_birth

            if 'name' in body:
                if new_name == "":
                    raise ValueError
                actor.name = new_name

            if 'full_name' in body:
                if new_full_name == "":
                    raise ValueError
                actor.full_name = new_full_name

            actor.update()

            return jsonify({
                "success": True,
                "actor_info": actor.long_info
            }), 200

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception as e:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).first()

        if actor is None:
            return abort(404)

        try:
            actor.delete()

            return jsonify({
                "success": True,
                "deleted_actor_id": actor.id
            }), 200

        except Exception as e:
            abort(500)

    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movies(payload):
        movies_query = Movie.query.order_by(Movie.id).all()

        return jsonify({
            "success": True,
            "movies": [movie.short_info for movie in movies_query]
        }), 200

    @app.route('/movies/<int:movie_id>')
    @requires_auth("get:movie-by-id")
    def get_movie_by_id(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()

        if movie is None:
            return abort(404)
        return jsonify({
            "success": True,
            "movie": movie.full_info
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth("post:movies")
    def create_movie(payload):
        try:
            body = request.get_json()
            new_title = body.get('title', None)
            new_release_year = body.get('release_year', None)
            new_duration = body.get('duration', None)
            new_imdb_rating = body.get('imdb_rating', None)
            new_cast = body.get('cast', None)

            if new_title == '' \
                    or new_release_year <= 0 \
                    or new_duration <= 0 \
                    or new_imdb_rating < 0 \
                    or new_imdb_rating > 10 \
                    or len(new_cast) == 0:
                raise TypeError

            new_movie = Movie(
                new_title,
                new_release_year,
                new_duration,
                new_imdb_rating
            )
            actors = Actor.query.filter(
                Actor.name.in_(new_cast)).all()

            if len(new_cast) == len(actors):
                new_movie.insert()
                for actor in actors:
                    actor_in_movie = ActorInMovie(new_movie.id, actor.id)
                    actor_in_movie.insert()
            else:
                raise ValueError

            return jsonify({
                "success": True,
                "created_movie_id": new_movie.id
            }), 201

        except (TypeError, KeyError, ValueError):
            abort(422)

        except Exception as e:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth("patch:movies")
    def update_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()

        if movie is None:
            return abort(404)

        try:
            body = request.get_json()
            new_title = body.get('title', None)
            new_release_year = body.get('release_year', None)
            new_duration = body.get('duration', None)
            new_imdb_rating = body.get('imdb_rating', None)
            new_cast = body.get('cast', None)

            if "title" in body:
                if new_title == "":
                    raise ValueError

                movie.title = new_title

            if "release_year" in body:
                if new_release_year <= 0:
                    raise ValueError

                movie.release_year = new_release_year

            if "duration" in body:
                if new_duration <= 0:
                    raise ValueError

                movie.duration = new_duration

            if "imdb_rating" in body:
                if new_imdb_rating < 0 \
                        or new_imdb_rating > 10:
                    raise ValueError

                movie.imdb_rating = new_imdb_rating

            if "cast" in body:
                if len(new_cast) == 0:
                    raise ValueError

                actors = Actor.query.filter(
                    Actor.name.in_(new_cast)).all()

                if len(new_cast) == len(actors):
                    movie.cast = actors
                else:
                    raise ValueError

            movie.update()

            return jsonify({
                "success": True,
                "movie_info": movie.long_info
            }), 200

        except (TypeError, ValueError, KeyError):
            abort(422)

        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()

        if movie is None:
            return abort(404)

        try:
            movie.delete()

            return jsonify({
                "success": True,
                "deleted_movie_id": movie.id
            }), 200

        except Exception:
            abort(500)

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        """
        Receive the raised authorization error and propagates it as response
        """
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(400)
    def error_handler(error):
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def resource_not_found_error_handler(error):
        return jsonify({
            'success': False,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(401)
    def resource_not_found_error_handler(error):
        return jsonify({
            'success': False,
            'message': 'Auth error'
        }), 401

    @app.errorhandler(403)
    def resource_not_found_error_handler(error):
        return jsonify({
            'success': False,
            'message': 'Forbidden'
        }), 403

    @app.errorhandler(405)
    def method_not_allowed_error_handler(error):
        '''
        Error handler for status code 405.
        '''
        return jsonify({
            'success': False,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error_handler(error):
        '''
        Error handler for status code 500.
        '''
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    return app

app = create_app()
