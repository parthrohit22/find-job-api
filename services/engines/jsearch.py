import requests

from config import RAPIDAPI_KEY, RAPIDAPI_HOST
from .base import JobEngine


BASE_URL = "https://jsearch.p.rapidapi.com/search"


class JSearchEngine(JobEngine):
    def fetch_jobs(self, query: str, country: str = "us", page: int = 1) -> list:
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }

        params = {
            "query": query,
            "country": country,
            "page": page,
            "num_pages": 1,
        }

        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data.get("data", [])