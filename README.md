# Find Job API

Find Job API is a production-ready REST API built with Flask that helps users search for jobs using real-time data from RapidAPI (JSearch).  
The API supports authentication, rate limiting, caching, filtering, and interactive documentation via Swagger.

This project was built as a backend-focused application with clean architecture, real-world constraints, and deployment readiness.

---
# Project Summary
	•	Built a production-ready Job Search REST API using Flask
	•	Integrated real-time job listings via RapidAPI (JSearch)
	•	Designed a clean modular architecture using Flask Blueprints
	•	Implemented API key authentication to secure all endpoints
	•	Added rate limiting to prevent abuse and protect external API usage
	•	Implemented in-memory caching to reduce duplicate external requests
	•	Normalized third-party job data into a consistent internal schema
	•	Included direct apply links for each job listing
	•	Documented the API using Swagger (Flasgger) with live execution support
	•	Deployed and validated the API in a production environment
	•	Version-controlled the project with Git and GitHub

⸻

How It Was Built
	•	Used Flask as the core web framework
	•	Structured the project using:
	•	routes/ for API endpoints
	•	services/ for external API integration
	•	utils/ for authentication, caching, rate limiting, and normalization
	•	Integrated RapidAPI (JSearch) using the requests library
	•	Protected endpoints with custom API key validation middleware
	•	Applied rate limiting per client IP
	•	Cached responses based on query parameters to improve performance
	•	Used Swagger (Flasgger) for interactive API documentation
	•	Tested endpoints using Postman and Swagger UI
	•	Managed environment configuration using environment variables
	•	Deployed using Gunicorn for production readiness

⸻

Tools & Technologies Used
	•	Python 3
	•	Flask
	•	Flasgger (Swagger / OpenAPI)
	•	RapidAPI (JSearch)
	•	Requests
	•	Gunicorn
	•	Git & GitHub
	•	Postman
	•	VS Code

⸻

Configuration & Environment
	•	API keys stored securely using environment variables
	•	Configuration isolated from application logic
	•	Production server run using Gunicorn
	•	Debug mode disabled for production
	•	.env and secrets excluded from version control

## Features

- Job search powered by JSearch (RapidAPI)
- API key–based authentication
- Rate limiting to prevent abuse
- In-memory caching for faster repeated queries
- Normalized and consistent job data
- Apply links included for each job
- Swagger (OpenAPI) documentation
- Ready for production deployment

---

## Tech Stack

- Python 3
- Flask
- Flasgger (Swagger UI)
- Requests
- RapidAPI (JSearch)
- Gunicorn (production server)
- Git & GitHub

---

## Project Structure

find-job-api/
│
├── app.py                  # Flask application entry point
├── config.py               # Configuration and environment handling
├── requirements.txt        # Python dependencies
│
├── routes/
│   ├── jobs.py             # /jobs endpoint
│   └── health.py           # health check endpoint
│
├── services/
│   └── jsearch.py          # RapidAPI JSearch integration
│
├── utils/
│   ├── auth.py             # API key authentication
│   ├── cache.py            # Caching logic
│   ├── rate_limiter.py     # Rate limiting logic
│   └── normalizer.py       # Job data normalization
│
└── README.md

---

## Authentication

All requests to the API require an API key.

The key must be passed in the request header:

X-API-Key: your-api-key

Requests without a valid API key will return a 401 Unauthorized response.

---

## Rate Limiting

The API enforces rate limiting per client IP to prevent abuse.  
If the limit is exceeded, the API returns:

HTTP 429 – Rate limit exceeded

---

## API Endpoints

### GET /jobs

Search for jobs using keywords and optional filters.

Required query parameter:
- query — job title or keyword (e.g. developer, cyber)

Optional query parameters:
- country — ISO-2 country code (default: us)
- page — page number for pagination (default: 1)
- remote — true or false
- type — employment type (FULLTIME or CONTRACT)

Example request:

GET /jobs?query=developer&country=us&remote=true

Required header:

X-API-Key: your-api-key

---

## Example Response

{
  "cached": false,
  "page": 1,
  "count": 10,
  "results": [
    {
      "id": "XacHlAyDYl96t7ASAAAAAA==",
      "title": "Backend Software Developer",
      "company": "Aperio Global",
      "location": "Washington",
      "employment_type": "Full-time",
      "remote": false,
      "apply_link": "https://www.example.com/apply",
      "apply_source": "Company Site",
      "apply_type": "direct"
    }
  ]
}

---

## Swagger Documentation

Interactive API documentation is available via Swagger.

Local:
http://127.0.0.1:5000/apidocs

Production:
https://your-deployment-url/apidocs

Swagger allows you to:
- Explore endpoints
- Provide query parameters
- Authenticate using API keys
- Execute requests directly from the browser

---

## Local Setup

1. Clone the repository

git clone https://github.com/parthrohit22/find-job-api.git
cd find-job-api

2. Create a virtual environment

python -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run the application

python app.py

The API will be available at:
http://127.0.0.1:5000

---

## Environment Variables

The following environment variables are required:

- RAPIDAPI_KEY — your RapidAPI key
- RAPIDAPI_HOST — JSearch API host

These should be stored securely and never committed to GitHub.

---

## Deployment

The API is designed to run behind Gunicorn in production and can be deployed on platforms such as Render, Railway, or similar PaaS providers.

Example production command:

gunicorn app:app

---

## Security Notes

- API keys must never be exposed publicly
- Environment variables should be managed securely
- Rate limiting is enforced to reduce abuse
- This API is not intended to be used as an open, unauthenticated service

---

## License

This project is for educational and portfolio purposes.

---

## Author

Parth Rohit  

GitHub: https://github.com/parthrohit22