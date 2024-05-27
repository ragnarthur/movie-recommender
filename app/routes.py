from flask import Flask, Blueprint, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

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

def get_genres():
    url = 'https://api.themoviedb.org/3/genre/movie/list'
    params = {
        'language': 'pt-BR'
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['genres']

# Define a global genre map
GENRE_MAP = {genre['id']: genre['name'] for genre in get_genres()}

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
        movie['vote_average'] = f"{movie['vote_average']:.1f}"  # Formatar a avaliação com uma casa decimal
        movie['director'], movie['cast'] = get_movie_credits(movie_id)
        movie['genres'] = ", ".join([GENRE_MAP[genre_id] for genre_id in movie['genre_ids']])

    return recommendations

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

def get_movie_credits(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits'
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    director = next((member['name'] for member in data['crew'] if member['job'] == 'Director'), 'N/A')
    cast = ', '.join([member['name'] for member in data['cast'][:3]])  # Pegue os 3 principais membros do elenco
    return director, cast

app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True)
