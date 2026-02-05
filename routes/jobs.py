from utils.auth import is_valid_api_key
from flask import Blueprint, request
from services.jsearch import get_jobs
from utils.normalizer import normalize_job
from utils.cache import get_cache, set_cache
from utils.rate_limiter import is_rate_limited

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/jobs")
def jobs():
        # 🔐 AUTHENTICATION
    api_key = request.headers.get("X-API-Key")
    if not api_key or not is_valid_api_key(api_key):
        return {"error": "unauthorised"}, 401

    # 🔴 RATE LIMIT FIRST
    client_ip = request.remote_addr
    if is_rate_limited(client_ip):
        return {"error": "rate limit exceeded"}, 429

    query = request.args.get("query")
    country = request.args.get("country", "us")
    page = int(request.args.get("page", 1))
    remote = request.args.get("remote")
    employment_type = request.args.get("type")

    if not query:
        return {"error": "query parameter is required"}, 400

    cache_key = f"{query}:{country}:{page}:{remote}:{employment_type}"
    cached = get_cache(cache_key)

    if cached:
        return {
            "cached": True,
            **cached
        }

    raw_jobs = get_jobs(query, country, page)
    jobs = [normalize_job(job) for job in raw_jobs]

    if remote is not None:
        remote = remote.lower() == "true"
        jobs = [job for job in jobs if job["remote"] == remote]

    if employment_type:
        employment_type = employment_type.upper()
        jobs = [
            job for job in jobs
            if job["employment_type"] == employment_type
        ]

    response = {
        "cached": False,
        "page": page,
        "count": len(jobs),
        "results": jobs
    }

    set_cache(cache_key, response, ttl=300)
    return response