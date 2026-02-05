import requests
import os
from .base import JobEngine
app_id = os.getenv("ADZUNA_APP_ID")
app_key = os.getenv("ADZUNA_APP_KEY")

if not app_id or not app_key:
    raise RuntimeError("Missing Adzuna API credentials")

class AdzunaEngine(JobEngine):
    def fetch_jobs(self, query, country="uk", page=1):
        country = country.lower()
        if country == "uk":
            country = "gb"

        page = max(1, page)

        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")

        if not app_id or not app_key:
            raise RuntimeError("Missing Adzuna API credentials")

        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": query,
            "results_per_page": 20,
            "content-type": "application/json",
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("Adzuna error:", response.status_code, response.text)

        response.raise_for_status()
        return response.json().get("results", [])