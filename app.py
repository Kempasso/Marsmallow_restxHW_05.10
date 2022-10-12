# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 4}
db = SQLAlchemy(app)
api = Api(app)
movies = api.namespace('/movies')


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movies.route('/')
class ShowMovies(Resource):
    def get(self):
        director_id = request.args.get('director_id', '')
        genre_id = request.args.get('genre_id', '')
        if director_id:
            movies_with_director_id = db.session.query(Movie).filter(Movie.director_id == director_id).all()
            json_movies = movies_schema.dump(movies_with_director_id)
            return json_movies, 200
        elif genre_id:
            movies_with_genre_id = db.session.query(Movie).filter(Movie.genre_id == genre_id).all()
            json_movies = movies_schema.dump(movies_with_genre_id)
            return json_movies, 200
        movies = db.session.query(Movie).all()
        json_movies = movies_schema.dump(movies)
        return json_movies, 200


@movies.route('/<int:movie_id>')
class ShowMovie(Resource):
    def get(self, movie_id):
        movie = db.session.query(Movie).filter(Movie.id == movie_id).one()
        if movie:
            json_movie = movie_schema.dump(movie)
            return json_movie, 200
        return {'message': 'Movie not found'}, 404


if __name__ == '__main__':
    app.run(debug=True)
