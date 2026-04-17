import os
from flask import Flask, request, jsonify
from models import db, Movie, Person

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'Database', 'MovieInfo.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# -------------------------
# 1. Search Movie Endpoint
# -------------------------
@app.route('/api/movies', methods=['GET'])
def search_movies():
    query = Movie.query

    # Filters
    year = request.args.get('year')
    genre = request.args.get('genre')
    person_name = request.args.get('person_name')
    type_ = request.args.get('type')

    if year:
        query = query.filter(Movie.year_released == int(year))
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    if type_:
        query = query.filter(Movie.type.ilike(f"%{type_}%"))
    if person_name:
        query = query.join(Movie.people).filter(Person.name.ilike(f"%{person_name}%"))

    movies = query.all()

    results = []
    for movie in movies:
        results.append({
            "Title": movie.title,
            "Year Released": movie.year_released,
            "Type": movie.type,
            "Genre": movie.genre,
            "List of People Associated": [p.name for p in movie.people]
        })

    return jsonify(results)

# -------------------------
# 2. Search Person Endpoint
# -------------------------
@app.route('/api/people', methods=['GET'])
def search_people():
    query = Person.query

    # Filters
    movie_title = request.args.get('movie_title')
    name = request.args.get('name')
    profession = request.args.get('profession')

    if name:
        query = query.filter(Person.name.ilike(f"%{name}%"))
    if profession:
        query = query.filter(Person.profession.ilike(f"%{profession}%"))
    if movie_title:
        query = query.join(Person.movies).filter(Movie.title.ilike(f"%{movie_title}%"))

    people = query.all()

    results = []
    for person in people:
        results.append({
            "Name": person.name,
            "Birth Year": person.birth_year,
            "Profession": person.profession,
            "Known for Titles": [m.title for m in person.movies]
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
