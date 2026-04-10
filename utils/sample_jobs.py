PAGE_SIZE = 20


SAMPLE_JOBS = [
    {
        "country_code": "us",
        "id": "sample-us-frontend-1",
        "title": "Frontend Developer",
        "company": "Northstar Commerce",
        "location": "Austin, TX",
        "remote": True,
        "work_mode": "remote",
        "distance_km": 8,
        "employment_type": "FULLTIME",
        "apply_link": "https://example.com/jobs/sample-us-frontend-1",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
    {
        "country_code": "us",
        "id": "sample-us-ui-2",
        "title": "UI Engineer",
        "company": "Cascade Health",
        "location": "Boston, MA",
        "remote": False,
        "work_mode": "hybrid",
        "distance_km": 12,
        "employment_type": "FULLTIME",
        "apply_link": "https://example.com/jobs/sample-us-ui-2",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
    {
        "country_code": "us",
        "id": "sample-us-fullstack-3",
        "title": "Full Stack Developer",
        "company": "BrightLayer Labs",
        "location": "New York, NY",
        "remote": False,
        "work_mode": "onsite",
        "distance_km": 5,
        "employment_type": "CONTRACT",
        "apply_link": "https://example.com/jobs/sample-us-fullstack-3",
        "apply_source": "LinkedIn",
        "apply_type": "redirect",
    },
    {
        "country_code": "us",
        "id": "sample-us-data-4",
        "title": "Data Analyst Intern",
        "company": "Riverbank Insights",
        "location": "Chicago, IL",
        "remote": False,
        "work_mode": "hybrid",
        "distance_km": 18,
        "employment_type": "INTERNSHIP",
        "apply_link": "https://example.com/jobs/sample-us-data-4",
        "apply_source": "Indeed",
        "apply_type": "redirect",
    },
    {
        "country_code": "us",
        "id": "sample-us-product-5",
        "title": "Product Designer",
        "company": "Foundry Systems",
        "location": "San Francisco, CA",
        "remote": True,
        "work_mode": "remote",
        "distance_km": 16,
        "employment_type": "FULLTIME",
        "apply_link": "https://example.com/jobs/sample-us-product-5",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
    {
        "country_code": "us",
        "id": "sample-us-backend-6",
        "title": "Backend Software Engineer",
        "company": "Pioneer Cloud",
        "location": "Seattle, WA",
        "remote": False,
        "work_mode": "onsite",
        "distance_km": 28,
        "employment_type": "FULLTIME",
        "apply_link": "https://example.com/jobs/sample-us-backend-6",
        "apply_source": "ZipRecruiter",
        "apply_type": "redirect",
    },
    {
        "country_code": "us",
        "id": "sample-us-qa-7",
        "title": "QA Automation Engineer",
        "company": "Copper Ridge",
        "location": "Denver, CO",
        "remote": False,
        "work_mode": "hybrid",
        "distance_km": 10,
        "employment_type": "PARTTIME",
        "apply_link": "https://example.com/jobs/sample-us-qa-7",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
    {
        "country_code": "gb",
        "id": "sample-gb-frontend-8",
        "title": "Frontend Angular Engineer",
        "company": "Camden Digital",
        "location": "London, UK",
        "remote": False,
        "work_mode": "hybrid",
        "distance_km": 7,
        "employment_type": "FULLTIME",
        "apply_link": "https://example.com/jobs/sample-gb-frontend-8",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
    {
        "country_code": "gb",
        "id": "sample-gb-qa-9",
        "title": "QA Automation Engineer",
        "company": "Bristol Fintech",
        "location": "Bristol, UK",
        "remote": False,
        "work_mode": "onsite",
        "distance_km": 14,
        "employment_type": "CONTRACT",
        "apply_link": "https://example.com/jobs/sample-gb-qa-9",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
    {
        "country_code": "gb",
        "id": "sample-gb-data-10",
        "title": "Data Engineer",
        "company": "Northern Analytics",
        "location": "Manchester, UK",
        "remote": True,
        "work_mode": "remote",
        "distance_km": 22,
        "employment_type": "FULLTIME",
        "apply_link": "https://example.com/jobs/sample-gb-data-10",
        "apply_source": "Adzuna",
        "apply_type": "redirect",
    },
    {
        "country_code": "gb",
        "id": "sample-gb-intern-11",
        "title": "Software Engineering Intern",
        "company": "Harbor Labs",
        "location": "Leeds, UK",
        "remote": False,
        "work_mode": "hybrid",
        "distance_km": 9,
        "employment_type": "INTERNSHIP",
        "apply_link": "https://example.com/jobs/sample-gb-intern-11",
        "apply_source": "Company Site",
        "apply_type": "direct",
    },
]


def _normalize_country(country: str) -> str:
    country = (country or "us").lower()
    return "gb" if country == "uk" else country


def _matches_query(job: dict, query: str) -> bool:
    tokens = [token for token in query.lower().split() if token]
    if not tokens:
        return True

    haystack = " ".join(
        [
            job.get("title", ""),
            job.get("company", ""),
            job.get("location", ""),
            job.get("employment_type", ""),
            job.get("work_mode", ""),
        ]
    ).lower()

    return all(token in haystack for token in tokens)


def search_sample_jobs(query: str, country: str, page: int) -> list[dict]:
    country_code = _normalize_country(country)
    matching_jobs = [
        {
            key: value
            for key, value in job.items()
            if key != "country_code"
        }
        for job in SAMPLE_JOBS
        if job["country_code"] == country_code and _matches_query(job, query)
    ]

    start = max(0, (max(1, page) - 1) * PAGE_SIZE)
    end = start + PAGE_SIZE
    return matching_jobs[start:end]
