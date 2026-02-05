from flasgger import swag_from
from flask import Blueprint, request
from services.jsearch import get_jobs
from utils.normalizer import normalize_job
from utils.cache import get_cache, set_cache
from utils.rate_limiter import is_rate_limited
from utils.auth import is_valid_api_key

jobs_bp = Blueprint("jobs", __name__)
@jobs_bp.route("/jobs", methods=["GET"])
def jobs():
    """
    Job Search Endpoint
    ---
    tags:
      - Jobs
    parameters:
      - name: X-API-Key
        in: header
        type: string
        required: true
        description: API key

      - name: query
        in: query
        type: string
        required: true
        description: Job title or keyword

      - name: country
        in: query
        type: string
        required: false
        default: us
        description: Country code (ISO-2)

      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number

      - name: remote
        in: query
        type: boolean
        required: false
        description: Filter remote jobs

      - name: type
        in: query
        type: string
        required: false
        description: FULLTIME or CONTRACT

    responses:
      200:
        description: Successful job search
      401:
        description: Unauthorized
      429:
        description: Rate limit exceeded
    """

    # AUTH
    api_key = request.headers.get("X-API-Key")
    if not api_key or not is_valid_api_key(api_key):
        return {"error": "unauthorized"}, 401

    # RATE LIMIT
    client_ip = request.remote_addr
    if is_rate_limited(client_ip):
        return {"error": "rate limit exceeded"}, 429

    query = request.args.get("query")
    if not query:
        return {"error": "query parameter is required"}, 400

    country = request.args.get("country", "us")
    page = int(request.args.get("page", 1))

    raw_jobs = get_jobs(query, country, page)
    jobs = [normalize_job(job) for job in raw_jobs]

    response = {
        "cached": False,
        "page": page,
        "count": len(jobs),
        "results": jobs
    }

    return response