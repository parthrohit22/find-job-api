def normalize_job(job):
    apply_link = (
        job.get("job_apply_link")
        or job.get("job_google_link")
        or job.get("employer_website")
    )

    if apply_link:
        if "linkedin.com" in apply_link:
            source = "LinkedIn"
        elif "indeed.com" in apply_link:
            source = "Indeed"
        elif "ziprecruiter.com" in apply_link:
            source = "ZipRecruiter"
        elif "google.com" in apply_link:
            source = "Google Jobs"
        else:
            source = "Company Site"
    else:
        source = None

    apply_type = "direct" if job.get("job_apply_link") else "redirect"

    # 👇 ORDER DEFINED HERE
    return {
        "id": job.get("job_id"),
        "title": job.get("job_title"),
        "company": job.get("employer_name"),
        "location": job.get("job_city"),
        "remote": job.get("job_is_remote", False),
        "employment_type": job.get("job_employment_type"),
        "apply_link": apply_link,
        "apply_source": source,
        "apply_type": apply_type
    }