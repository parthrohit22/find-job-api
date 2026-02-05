def normalize_job(job):
    apply_link = (
        job.get("job_apply_link")
        or job.get("job_google_link")
        or job.get("employer_website")
    )

    source = None
    if apply_link:
        if "linkedin.com" in apply_link:
            source = "LinkedIn"
        elif "indeed.com" in apply_link:
            source = "Indeed"
        elif "google.com" in apply_link:
            source = "Google Jobs"
        else:
            source = "Company Site"

    return {
        "id": job.get("job_id"),
        "title": job.get("job_title"),
        "company": job.get("employer_name"),
        "location": job.get("job_city"),
        "employment_type": job.get("job_employment_type"),
        "remote": job.get("job_is_remote", False),
        "apply_link": apply_link,
        "apply_source": source,
        "apply_type": "direct" if job.get("job_apply_link") else "redirect"
    }