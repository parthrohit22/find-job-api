## Find Job API

Find Job API is a production-ready REST API built with Flask that helps users search for jobs using real-time data from RapidAPI (JSearch).
The API supports authentication, rate limiting, caching, filtering, and interactive documentation via Swagger.

This project focuses on backend engineering practices, clean architecture, and production readiness.


## Project Summary
	•	Built a production-ready Job Search REST API using Flask
	•	Integrated real-time job listings via RapidAPI (JSearch)
	•	Designed a modular architecture using Flask Blueprints
	•	Secured endpoints using API key authentication
	•	Implemented rate limiting to prevent abuse
	•	Added in-memory caching to reduce duplicate external requests
	•	Normalized third-party job data into a consistent schema
	•	Included direct apply links for each job listing
	•	Documented the API using Swagger (Flasgger)
	•	Deployed and validated the API in a production environment
	•	Managed source code using Git and GitHub
	•	Added multi-engine job sourcing with country-based engine selection
	•	Integrated Adzuna API for UK-specific job listings
	•	Improved UK job accuracy with city-level filtering
	•	Implemented engine abstraction to support future job data sources
	•	Ensured consistent response schema across different job providers

## How It Was Built
	•	Flask used as the core web framework
	•	Project structured into:
	•	routes (API endpoints)
	•	services (external API integration)
	•	utils (authentication, caching, rate limiting, normalization)
	•	RapidAPI (JSearch) integrated using the requests library
	•	API key validation implemented at the request level
	•	Rate limiting applied per client IP
	•	Responses cached using query-based keys
	•	Swagger used for interactive API documentation
	•	Endpoints tested using Postman and Swagger UI
	•	Environment variables used for configuration
	•	Gunicorn used for production execution
	•	Implemented an engine-based architecture to support multiple job providers
	•	Used Adzuna API for UK job searches and RapidAPI (JSearch) for US jobs
	•	Dynamically selected job source engine based on country parameter
	•	Normalized job data from different providers into a single response format
	•	Added city-based filtering for improved location accuracy



## Tools & Technologies Used
	•	Python 3
	•	Flask
	•	Flasgger (Swagger / OpenAPI)
	•	RapidAPI (JSearch)
	•	Adzuna Jobs API (UK job data)
	•	Requests
	•	Gunicorn
	•	Git & GitHub
	•	Postman
	•	VS Code


## Configuration & Environment
	•	API keys stored in environment variables
	•	Configuration isolated from application logic
	•	Debug mode disabled in production
	•	Secrets and .env files excluded from version control

## API Endpoint Overview

GET /jobs

Description:
Search for jobs using keywords and optional filters.

Required query parameter:
query — job title or keyword (example: developer, cyber)

Optional query parameters:
country — ISO-2 country code (default: us)
page — page number (default: 1)
remote — true or false
type — FULLTIME or CONTRACT

Required request header:
X-API-Key: your-api-key


## Example Request (plain text)

GET /jobs?query=developer&country=us&remote=true
X-API-Key: your-api-key


## Example Response (plain text)

{
“cached”: false,
“page”: 1,
“count”: 10,
“results”: [
{
“id”: “XacHlAyDYl96t7ASAAAAAA==”,
“title”: “Backend Software Developer”,
“company”: “Aperio Global”,
“location”: “Washington”,
“employment_type”: “Full-time”,
“remote”: false,
“apply_link”: “https://www.example.com/apply”,
“apply_source”: “Company Site”,
“apply_type”: “direct”
}
]
}

## Job Data Sources

US job listings are sourced using RapidAPI (JSearch).
UK job listings are sourced using the Adzuna Jobs API.

The API automatically selects the appropriate data source based on the country parameter while maintaining a consistent response structure.

## Swagger Documentation

Local:
http://127.0.0.1:5000/apidocs

Production:
https://your-deployment-url/apidocs

Swagger allows interactive exploration, authentication via API key, and live execution of requests.


## Local Setup

Clone repository
git clone https://github.com/parthrohit22/find-job-api.git
cd find-job-api

Create virtual environment
python -m venv venv
source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Run application
python app.py

## Environment Variables

RAPIDAPI_KEY — RapidAPI key
RAPIDAPI_HOST — JSearch API host

ADZUNA_APP_ID — Adzuna application ID (UK jobs)
ADZUNA_APP_KEY — Adzuna API key

These must never be committed to GitHub.


## Deployment

The API is designed to run behind Gunicorn in production.

Command:
gunicorn app:app


# Security Notes
	•	API keys must never be exposed publicly
	•	Environment variables must be handled securely
	•	Rate limiting reduces abuse
	•	This API is not intended as an open public service
	•	Third-party API credentials are managed using environment variables only

## License

This project is for educational and portfolio purposes.

## Author

Parth Rohit
GitHub: https://github.com/parthrohit22
