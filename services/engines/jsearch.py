import requests

from config import RAPIDAPI_KEY, RAPIDAPI_HOST
from .base import JobEngine


BASE_URL = "https://jsearch.p.rapidapi.com/search"


class JSearchEngine(JobEngine):
    def fetch_jobs(
        self,
        query: str,
        country: str = "us",
        page: int = 1,
        filters: dict | None = None
    ) -> list:
        filters = filters or {}
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
        }

        params = {
            "query": self._build_query(query, filters),
            "country": country,
            "page": page,
            "num_pages": 1,
        }

        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        return data.get("data", [])

    def _build_query(self, query: str, filters: dict) -> str:
        search_parts = [query.strip()]

        location = (filters.get("location") or "").strip()
        work_mode = (filters.get("work_mode") or "").strip().lower()
        job_type = (filters.get("type") or "").strip().lower()

        if job_type == "internship":
            search_parts.append("internship")

        if work_mode in {"remote", "hybrid", "onsite"}:
            search_parts.append(work_mode)

        if location:
            search_parts.append(location)

        return " ".join(part for part in search_parts if part)
