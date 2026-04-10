# Find Job API

A production-style REST API built with Flask that aggregates job listings from multiple providers and exposes them through a unified, normalized interface.

The API integrates external job data sources, applies authentication, rate limiting, and caching, and provides interactive API documentation via Swagger.

This project focuses on backend engineering practices, modular architecture, and production-style API design.


## Features

- REST API built with Flask
- Angular frontend workspace with Bootstrap styling
- Multi-provider job sourcing
- SQLite-backed user accounts with generated API keys
- Request rate limiting
- In-memory caching
- Consistent job data normalization
- Country-based engine selection
- Frontend routing with protected pages
- Browser-persisted saved jobs, notes, and search history
- Location, distance, work-mode, and internship filters
- Interactive Swagger documentation
- Modular backend architecture

## System Architecture

The API follows a layered backend architecture where HTTP requests flow through the API layer, into service logic, and then to external job provider engines.
```
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

## Architecture

The application follows a modular service-oriented structure.
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
│   └── engines/
│       ├── base.py
│       ├── jsearch.py
│       └── adzuna.py
│
├── utils/
│   ├── auth.py
│   ├── cache.py
│   ├── rate_limiter.py
│   └── normalizer.py
│
└── README.md
```
Responsibilities of each layer:

routes/
Handles HTTP requests and API endpoints.

services/
Handles external API integrations and engine selection.

utils/
Contains reusable utilities such as authentication, caching,
rate limiting, and job data normalization.

## Technologies Used

- Python 3
- Flask
- Flasgger (Swagger / OpenAPI)
- RapidAPI JSearch
- Adzuna Jobs API
- Requests
- Gunicorn
- Git & GitHub
- Postman


## API Endpoint

### GET /api/jobs

Search for jobs using keywords and optional filters.

### Required Header

X-API-Key: your-api-key

### Required Query Parameter

query

Example:

/api/jobs?query=developer

### Optional Query Parameters
```
| Parameter | Description | Default |
|----------|-------------|--------|
| country | ISO-2 country code | us |
| location | City or region keyword | |
| distance | Radius in kilometers | |
| page | Page number | 1 |
| work_mode | remote, hybrid, onsite | |
| type | FULLTIME, PARTTIME, CONTRACT, INTERNSHIP | |
```

## Example Request

GET /api/jobs?query=developer&country=us&location=Austin&distance=20&work_mode=remote&type=FULLTIME
X-API-Key: your-api-key

## Example Response
```
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
"work_mode": "remote",
"distance_km": 8,
“employment_type”: “Full-time”,
“remote”: false,
“apply_link”: “https://www.example.com/apply”,
“apply_source”: “Company Site”,
“apply_type”: “direct”
}
]
}
```

## Job Data Sources
```
Country      Provider

US           RapidAPI (JSearch)
UK           Adzuna Jobs API
```
The API automatically selects the correct engine based on the country parameter while maintaining a consistent response schema.


## Swagger Documentation

Swagger provides interactive API documentation and testing.

Local:
```
http://127.0.0.1:5001/apidocs
```
Production:
```
https://your-deployment-url/apidocs
```
## Local Setup

Clone the repository

git clone https://github.com/parthrohit22/find-job-api.git
cd find-job-api

Create virtual environment
```
python -m venv venv
source venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```

Create the Angular app dependencies
```
cd frontend
npm install
cd ..
```

Use an LTS Node.js release for Angular work. Angular CLI 21 warns that Node `v25.x` is
unsupported and may cause local builds to fail unexpectedly.

During local development, if a live job provider is unavailable, the backend falls back to bundled
sample job data so the frontend can still be exercised end to end.

Create an account in the Angular UI before searching. The backend stores users in `data/jobsearch.sqlite3`
and issues a fresh API key on signup or login.

Run application
```
python app.py or python3 app.py
```

Run the Angular frontend in development
```
cd frontend
npm start
```

The Flask API runs on `http://127.0.0.1:5001`.

The Angular dev server runs on `http://localhost:4200` and proxies `/api/*` requests to the Flask
API on port `5001`.

Build the frontend for Flask hosting
```
cd frontend
npm run build
cd ..
python app.py
```

After the build, Flask serves the Angular app at `http://127.0.0.1:5001/`.
## Environment Variables

Create a `.env` file in the project root.

RAPIDAPI_KEY=your_key
RAPIDAPI_HOST=jsearch.p.rapidapi.com

ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key

These credentials must never be committed to GitHub.


## Deployment

The API is designed to run behind Gunicorn.

gunicorn app:app

## Security Notes

- API keys required for all requests
- Frontend account creation uses `/api/auth/register`
- Frontend sign-in uses `/api/auth/login`
- Passwords and session API keys are stored as salted SHA-256 hashes
- Rate limiting applied per client IP
- Secrets stored using environment variables
- `.env` files excluded from Git
- Third-party credentials never stored in source code


## Author
Parth Rohit
