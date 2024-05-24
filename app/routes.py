from flask import Flask, Blueprint, render_template, request
import requests
from datetime import datetime
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

main = Blueprint('main', __name__)

API_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNWQ1MDE5ZDY1NzczZmQ0MzgzNDgzYWQxNzk5NWM1NiIsInN1YiI6IjY2NTBhMThlODk0ZDRlMDdjNzA2OTQ5MSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.6ECZy1xjzSvs8vmpAllRoV3LyXXxudIPDoJMj8pDeko'

HEADERS = {
    "accept": "application/json",
    "Authorization": API_TOKEN
}

@main.app_template_filter('format_date')
def format_date(value):
    date = datetime.strptime(value, '%Y-%m-%d')
    return date.strftime('%d/%m/%Y')

@main.route('/')
def home():
    genres = get_genres()
    return render_template('home.html', genres=genres)

@main.route('/recommend', methods=['POST'])
def recommend():
    genre_id = request.form.get('genre')
    year = request.form.get('year')
    rating = request.form.get('rating')
    
    min_rating, max_rating = (None, None)
    if rating == '0-5':
        min_rating, max_rating = 0, 5
    elif rating == '5-10':
        min_rating, max_rating = 5, 10
    
    recommendations = get_recommendations(genre_id, year, min_rating, max_rating)
    return render_template('recommendations.html', recommendations=recommendations)

@cache.cached(timeout=3600, key_prefix='genres')
def get_genres():
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'language': 'pt-BR'
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['genres']

@cache.cached(timeout=3600, key_prefix=lambda: request.form.get('genre') + request.form.get('year') + request.form.get('rating'))
def get_recommendations(genre_id, year, min_rating, max_rating):
    url = 'https://api.themoviedb.org/3/discover/movie'
    params = {
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 1000,
        'with_genres': genre_id,
        'primary_release_year': year,
        'vote_average.gte': min_rating,
        'vote_average.lte': max_rating,
        'language': 'pt-BR'
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    recommendations = data['results'][:10]  # Retorna os top 10 mais votados

    for movie in recommendations:
        movie_id = movie['id']
        trailer_url = get_trailer_url(movie_id)
        movie['trailer_url'] = trailer_url

    return recommendations

@cache.cached(timeout=3600, key_prefix=lambda movie_id: str(movie_id))
def get_trailer_url(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos'
    params = {
        'language': 'en-US'  # A maioria dos trailers está disponível em inglês
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    for video in data['results']:
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            return f'https://www.youtube.com/watch?v={video["key"]}'
    return None

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
