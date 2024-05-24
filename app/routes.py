from flask import Blueprint, render_template, request
import requests
from datetime import datetime

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
    return data['results'][:20]  # Retorna os top 20 mais votados
