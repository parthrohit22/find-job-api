import os
import requests

from .base import JobEngine


class AdzunaEngine(JobEngine):
    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def fetch_jobs(
        self,
        query: str,
        country: str = "uk",
        page: int = 1,
        filters: dict | None = None
    ) -> list:
        filters = filters or {}
        country = country.lower()
        if country == "uk":
            country = "gb"

        page = max(1, page)

        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")

        if not app_id or not app_key:
            raise RuntimeError("Missing Adzuna API credentials")

        url = f"{self.BASE_URL}/{country}/search/{page}"

        search_query = query.strip()
        work_mode = (filters.get("work_mode") or "").strip().lower()
        job_type = (filters.get("type") or "").strip().lower()
        location = (filters.get("location") or "").strip()
        distance = filters.get("distance")

        if job_type == "internship":
            search_query = f"{search_query} internship".strip()

        if work_mode in {"remote", "hybrid", "onsite"}:
            search_query = f"{search_query} {work_mode}".strip()

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": search_query,
            "results_per_page": 20,
            "content-type": "application/json",
        }

        if location:
            params["where"] = location

        if distance is not None:
            params["distance"] = distance

        if job_type == "fulltime":
            params["full_time"] = 1
        elif job_type == "parttime":
            params["part_time"] = 1
        elif job_type == "contract":
            params["contract"] = 1

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(f"Adzuna API error: {response.status_code} - {response.text}")

        data = response.json()
        return data.get("results", [])
