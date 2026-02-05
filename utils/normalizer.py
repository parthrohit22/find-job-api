def normalize_job(job):
    # =========================
    # JSEARCH FORMAT
    # =========================
    if "job_id" in job:
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

        return {
            "id": job.get("job_id"),
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_city") or job.get("job_country"),
            "remote": job.get("job_is_remote", False),
            "employment_type": job.get("job_employment_type"),
            "apply_link": apply_link,
            "apply_source": source,
            "apply_type": apply_type
        }

    # =========================
    # ADZUNA FORMAT
    # =========================
    apply_link = job.get("redirect_url")

    if apply_link:
        if "linkedin.com" in apply_link:
            source = "LinkedIn"
        elif "indeed.com" in apply_link:
            source = "Indeed"
        else:
            source = "Adzuna"
    else:
        source = None

    return {
        "id": job.get("id"),
        "title": job.get("title"),
        "company": job.get("company", {}).get("display_name"),
        "location": job.get("location", {}).get("display_name"),
        "remote": False,
        "employment_type": job.get("contract_time"),
        "apply_link": apply_link,
        "apply_source": source,
        "apply_type": "redirect"
    }