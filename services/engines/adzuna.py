import os
import requests

from .base import JobEngine


class AdzunaEngine(JobEngine):
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def fetch_jobs(self, query: str, country: str = "uk", page: int = 1) -> list:
        country = country.lower()
        if country == "uk":
            country = "gb"

        page = max(1, page)

        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")

        if not app_id or not app_key:
            raise RuntimeError("Missing Adzuna API credentials")

        url = f"{self.BASE_URL}/{country}/search/{page}"

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": query,
            "results_per_page": 20,
            "content-type": "application/json",
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(f"Adzuna API error: {response.status_code} - {response.text}")

        data = response.json()
        return data.get("results", [])