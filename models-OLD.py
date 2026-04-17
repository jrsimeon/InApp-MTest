# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# # Association table for many-to-many relationship between movies and people
# movie_people = db.Table(
#     'movie_people',
#     db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'), primary_key=True),
#     db.Column('person_id', db.Integer, db.ForeignKey('people.id'), primary_key=True)
# )

# class Movie(db.Model):
#     __tablename__ = 'movies'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     year_released = db.Column(db.Integer)
#     type = db.Column(db.String(50))   # Movie, TV Series, Documentary
#     genre = db.Column(db.String(100))

#     people = db.relationship('Person', secondary=movie_people, back_populates='movies')

# class Person(db.Model):
#     __tablename__ = 'people'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(200), nullable=False)
#     birth_year = db.Column(db.Integer)
#     profession = db.Column(db.String(100))  # Writer, Director, Actor

#     movies = db.relationship('Movie', secondary=movie_people, back_populates='people')
