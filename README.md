# Find Job API

A production-style REST API built with Flask that aggregates job listings from multiple providers and exposes them through a unified, normalized interface.

The API integrates external job data sources, applies authentication, rate limiting, and caching, and provides interactive API documentation via Swagger.

This project focuses on backend engineering practices, modular architecture, and production-style API design.


## Features

- REST API built with Flask
- Multi-provider job sourcing
- API key authentication
- Request rate limiting
- In-memory caching
- Consistent job data normalization
- Country-based engine selection
- Interactive Swagger documentation
- Modular backend architecture


## Architecture

The application follows a modular service-oriented structure.
```
find-job-api/
│
├── app.py
├── config.py
├── requirements.txt
│
├── routes/
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

### GET /jobs

Search for jobs using keywords and optional filters.


### Required Header

X-API-Key: your-api-key

### Required Query Parameter

query

Example:

/jobs?query=developer

### Optional Query Parameters
```
| Parameter | Description | Default |
|----------|-------------|--------|
| country | ISO-2 country code | us |
| page | Page number | 1 |
| remote | true or false | false |
| type | FULLTIME or CONTRACT | |
```

## Example Request

GET /jobs?query=developer&country=us&remote=true
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
http://127.0.0.1:5000/apidocs
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
Run application
```
python app.py or python3 app.py
```
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
- Rate limiting applied per client IP
- Secrets stored using environment variables
- `.env` files excluded from Git
- Third-party credentials never stored in source code


## Author
Parth Rohit

