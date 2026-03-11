def normalize_job(job: dict) -> dict:

    def detect_source(link: str | None) -> str | None:
        if not link:
            return None

        if "linkedin.com" in link:
            return "LinkedIn"
        if "indeed.com" in link:
            return "Indeed"
        if "ziprecruiter.com" in link:
            return "ZipRecruiter"
        if "google.com" in link:
            return "Google Jobs"

        return "Company Site"

    # RapidAPI job format
    if "job_id" in job:
        apply_link = (
            job.get("job_apply_link")
            or job.get("job_google_link")
            or job.get("employer_website")
        )

        return {
            "id": job.get("job_id"),
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city") or job.get("job_country"),
            "remote": job.get("job_is_remote", False),
            "employment_type": job.get("job_employment_type"),
            "apply_link": apply_link,
            "apply_source": detect_source(apply_link),
            "apply_type": "direct" if job.get("job_apply_link") else "redirect",
        }

    # Adzuna job format
    apply_link = job.get("redirect_url")

    return {
        "id": job.get("id"),
        "title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "remote": False,
        "employment_type": job.get("contract_time"),
        "apply_link": apply_link,
        "apply_source": detect_source(apply_link) if apply_link else "Adzuna",
        "apply_type": "redirect",
    }