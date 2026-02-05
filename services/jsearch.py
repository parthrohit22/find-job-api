import requests
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

BASE_URL = "https://jsearch.p.rapidapi.com/search"

def get_jobs(query, country="us", page=1):
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    params = {
        "query": query,
        "country": country,
        "page": page,
        "num_pages": 1
    }

    response = requests.get(BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]