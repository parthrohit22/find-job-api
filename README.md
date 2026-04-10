# Find Job API

A production-style job search platform built with **Flask** and an **Angular frontend**.  
It aggregates job listings from multiple providers and exposes them through a unified, normalized interface.

The backend applies authentication, rate limiting, provider selection, and fallback handling, while the frontend provides search, saved jobs, notes, and activity views.

## Features

- Flask REST API
- Angular frontend with Bootstrap styling
- Multi-provider job sourcing
- Country-based engine selection
- SQLite-backed user accounts with generated API keys
- API key authentication for protected endpoints
- Request rate limiting
- In-memory caching
- Consistent job data normalization
- Location, distance, work-mode, and internship filters
- Frontend routing with protected pages
- Browser-persisted saved jobs, notes, and search history
- Interactive Swagger documentation
- Modular backend architecture


## System Architecture

Requests flow from the Angular client into the Flask API, then through service logic and provider-specific engines.

```text
Angular Client
   |
   v
Flask API (routes)
   |
   v
Service Layer
   |
   v
Job Engines
   |        |
   v        v
JSearch   Adzuna
```

Project Structure
```
find-job-api/
│
├── app.py
├── config.py
├── requirements.txt
├── frontend/
│
├── routes/
│   ├── auth.py
│   ├── health.py
│   └── jobs.py
│
├── services/
│   ├── engine_factory.py
│   ├── user_store.py
│   └── engines/
│       ├── base.py
│       ├── jsearch.py
│       └── adzuna.py
│
├── utils/
│   ├── auth.py
│   ├── cache.py
│   ├── rate_limiter.py
│   ├── normalizer.py
│   └── sample_jobs.py
│
├── data/
└── README.md
````

Layer responsibilities

routes/
Handles HTTP requests and API endpoints.

services/
Handles provider integrations, engine selection, and user storage.

utils/
Contains reusable utilities such as authentication, caching, rate limiting, normalization, and development sample data.


Technologies Used
	•	Python 3
	•	Flask
	•	Angular
	•	Bootstrap
	•	Flasgger (Swagger / OpenAPI)
	•	RapidAPI JSearch
	•	Adzuna Jobs API
	•	Requests
	•	SQLite
	•	Gunicorn
	•	Git & GitHub
	•	Postman


Authentication

The frontend supports account registration and login through:
	•	POST /api/auth/register
	•	POST /api/auth/login

Authenticated users receive an API key, which must be sent in the X-API-Key header when calling protected job search endpoints.

Legacy API keys are also supported for compatibility.


API Endpoints

GET /api/jobs

Search for jobs using keywords and optional filters.

Required header
X-API-Key: your-api-key

Required query parameter
query

Optional query parameters
	•	country — ISO-2 country code (default: us)
	•	location — city or region keyword
	•	distance — radius in kilometers
	•	page — page number (default: 1)
	•	work_mode — remote, hybrid, or onsite
	•	type — FULLTIME, PARTTIME, CONTRACT, or INTERNSHIP

Example request

GET /api/jobs?query=developer&country=us&location=Austin&distance=20&work_mode=remote&type=FULLTIME
X-API-Key: your-api-key

Example response
```
{
  "cached": false,
  "query": "developer",
  "country": "us",
  "filters": {
    "location": "Austin",
    "distance": 20,
    "work_mode": "remote",
    "type": "FULLTIME"
  },
  "page": 1,
  "count": 10,
  "results": [
    {
      "id": "XacHlAyDYl96t7ASAAAAAA==",
      "title": "Backend Software Developer",
      "company": "Aperio Global",
      "location": "Washington",
      "work_mode": "remote",
      "employment_type": "Full-time",
      "remote": false,
      "apply_link": "https://www.example.com/apply",
      "apply_source": "Company Site",
      "apply_type": "direct"
    }
  ],
  "source": "provider",
  "warning": null
}
```

Job Data Sources
	•	US — RapidAPI (JSearch)
	•	UK — Adzuna Jobs API

The backend selects the provider based on the country parameter while returning a consistent normalized schema.


Swagger Documentation

Swagger provides interactive API documentation and testing.

Local
http://127.0.0.1:5001/apidocs

Production
https://your-deployment-url/apidocs


Frontend Notes
	•	Create an account in the Angular UI before searching
	•	User records are stored locally in data/jobsearch.sqlite3
	•	Saved jobs, notes, and search history are persisted in the browser
	•	Protected frontend pages require login


Local Setup

1. Clone the repository

git clone https://github.com/parthrohit22/find-job-api.git
cd find-job-api

2. Create a virtual environment

python -m venv venv
source venv/bin/activate

3. Install backend dependencies

pip install -r requirements.txt

4. Install frontend dependencies

cd frontend
npm install
cd ..

Use an LTS Node.js release for Angular development. Angular CLI 21 may warn that Node v25.x is unsupported.

5. Configure environment variables

Create a .env file in the project root:

RAPIDAPI_KEY=your_key
RAPIDAPI_HOST=jsearch.p.rapidapi.com
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key

These credentials must never be committed to GitHub.

6. Run the backend

python app.py

The Flask API runs on:
http://127.0.0.1:5001

7. Run the Angular frontend in development

cd frontend
npm start

The Angular dev server runs on:
http://localhost:4200

During development, /api/* requests are proxied to the Flask backend on port 5001.


Frontend Build for Flask Hosting

To build the frontend and let Flask serve it:

cd frontend
npm run build
cd ..
python app.py

After the build, Flask serves the Angular app at:

http://127.0.0.1:5001/


Development Notes
	•	If a live provider is unavailable during development, the backend can fall back to local sample job data so the frontend remains usable
	•	Sample fallback is intended for development convenience
	•	Legacy API keys remain supported for compatibility


Deployment

The backend is designed to run behind Gunicorn.

gunicorn app:app


Security Notes
	•	API keys are required for protected job search requests
	•	Frontend account creation uses /api/auth/register
	•	Frontend sign-in uses /api/auth/login
	•	Passwords and session API keys are stored as salted SHA-256 hashes
	•	Rate limiting is applied per client IP
	•	Secrets are stored using environment variables
	•	.env files are excluded from Git
	•	Third-party credentials are never stored in source code

Author

Parth Rohit

