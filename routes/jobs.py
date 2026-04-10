from flask import Blueprint, request
from services.engine_factory import get_engine
from services.user_store import find_user_by_api_key
from utils.normalizer import normalize_job
from utils.rate_limiter import is_rate_limited
from utils.auth import is_legacy_api_key
from utils.sample_jobs import search_sample_jobs


jobs_bp = Blueprint("jobs", __name__)


def _parse_bool(value: str | None) -> bool:
    if value is None:
        return False

    return value.lower() in {"1", "true", "yes", "on"}


def _normalize_employment_type(value: str | None) -> str:
    if not value:
        return ""

    return "".join(char for char in value.lower() if char.isalnum())


def _use_sample_fallback() -> bool:
    return True


def _parse_distance(value: str | None) -> int | None:
    if value is None or not value.strip():
        return None

    distance = int(value)
    return max(0, distance)


def _parse_work_mode(value: str | None, remote_value: str | None) -> str:
    work_mode = (value or "").strip().lower()

    if not work_mode and remote_value is not None:
        return "remote" if _parse_bool(remote_value) else "onsite"

    if work_mode not in {"", "remote", "hybrid", "onsite"}:
        raise ValueError("work_mode must be one of remote, hybrid, or onsite")

    return work_mode


def _matches_location(job: dict, location: str) -> bool:
    if not location:
        return True

    searchable = " ".join(
        [
            job.get("location") or "",
            job.get("title") or "",
            job.get("company") or "",
        ]
    ).lower()
    return location.lower() in searchable


def _matches_distance(job: dict, distance: int | None) -> bool:
    if distance is None:
        return True

    job_distance = job.get("distance_km")
    if job_distance is None:
        return True

    try:
        return float(job_distance) <= float(distance)
    except (TypeError, ValueError):
        return True


def _matches_type(job: dict, job_type: str) -> bool:
    if not job_type:
        return True

    normalized_type = _normalize_employment_type(job_type)
    haystack = _normalize_employment_type(job.get("employment_type"))
    title = _normalize_employment_type(job.get("title"))

    return normalized_type in haystack or normalized_type in title


def _matches_work_mode(job: dict, work_mode: str) -> bool:
    if not work_mode:
        return True

    job_work_mode = (job.get("work_mode") or "").strip().lower()
    if work_mode == "remote":
        return bool(job.get("remote")) or job_work_mode == "remote"

    if work_mode == "hybrid":
        return job_work_mode == "hybrid"

    return job_work_mode == "onsite" or (not bool(job.get("remote")) and job_work_mode != "hybrid")


@jobs_bp.route("/jobs", methods=["GET"])
@jobs_bp.route("/api/jobs", methods=["GET"])
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

      - name: location
        in: query
        type: string
        required: false
        description: City or region keyword

      - name: distance
        in: query
        type: integer
        required: false
        description: Search radius in kilometers

      - name: type
        in: query
        type: string
        required: false
        description: FULLTIME, PARTTIME, CONTRACT, or INTERNSHIP

      - name: work_mode
        in: query
        type: string
        required: false
        description: remote, hybrid, or onsite

    responses:
      200:
        description: Successful job search
      401:
        description: Unauthorized
      429:
        description: Rate limit exceeded
    """

    # API key authentication
    api_key = (request.headers.get("X-API-Key") or "").strip()
    user = find_user_by_api_key(api_key) if api_key else None
    if not api_key or (not user and not is_legacy_api_key(api_key)):
        return {"error": "unauthorized"}, 401

    # Rate limiting
    client_ip = request.remote_addr
    if is_rate_limited(client_ip):
        return {"error": "rate limit exceeded"}, 429

    # Required query parameter
    query = request.args.get("query")
    if not query:
        return {"error": "query parameter is required"}, 400

    country = request.args.get("country", "us")
    location = request.args.get("location", "").strip()
    job_type = request.args.get("type", "").strip()

    try:
        page = max(1, int(request.args.get("page", 1)))
        distance = _parse_distance(request.args.get("distance"))
        work_mode = _parse_work_mode(request.args.get("work_mode"), request.args.get("remote"))
    except ValueError:
        return {"error": "page and distance must be valid integers; work_mode must be remote, hybrid, or onsite"}, 400

    engine = get_engine(country)

    source = "provider"
    warning = None

    try:
        raw_jobs = engine.fetch_jobs(
            query,
            country,
            page,
            {
                "location": location,
                "distance": distance,
                "type": job_type,
                "work_mode": work_mode,
            },
        )
        jobs = [normalize_job(job) for job in raw_jobs]
    except Exception as exc:
        if not _use_sample_fallback():
            return {"error": "job provider unavailable", "details": str(exc)}, 502

        jobs = search_sample_jobs(query, country, page)
        source = "sample_fallback"
        warning = (
            "Live job provider is unavailable right now. Showing local sample jobs so the app "
            "remains usable in development."
        )

    jobs = [
        job for job in jobs
        if _matches_location(job, location)
        and _matches_distance(job, distance)
        and _matches_type(job, job_type)
        and _matches_work_mode(job, work_mode)
    ]

    response = {
        "cached": False,
        "query": query,
        "country": country,
        "filters": {
            "location": location,
            "distance": distance,
            "work_mode": work_mode,
            "type": job_type,
        },
        "page": page,
        "count": len(jobs),
        "results": jobs,
        "source": source,
        "warning": warning,
    }

    return response
