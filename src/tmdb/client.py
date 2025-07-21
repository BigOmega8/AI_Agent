import requests
from django.conf import settings

# Define the API key and headers for TMDB requests
def get_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_API_KEY}"
    }

def search_movie(query:str, page:int=1, raw=False):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "query": query,
        "page": page,
        "include_adult": "false",
        "language": "en-US"
    }
    headers = get_headers()
    if raw:
        return response
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def movie_details(movie_id:int, raw=False):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "include_adult": "false",
        "language": "en-US"
    }
    headers = get_headers()
    if raw:
        return response
    response = requests.get(url, headers=headers, params=params)
    return response.json()