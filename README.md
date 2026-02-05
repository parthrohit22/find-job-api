#JOB SEARCH API
==============

A production-ready Job Search API built with Flask that aggregates job listings
from external sources, normalizes inconsistent data, and exposes a clean,
secure API for clients.

The API uses JSearch (RapidAPI) as its data source and demonstrates real-world
backend engineering practices such as authentication, rate limiting, caching,
external API abstraction, and cloud deployment.


#FEATURES
--------

- Job search powered by JSearch (RapidAPI)
- Clean and normalized job data schema
- Apply links with intelligent fallback logic
- API key–based authentication
- Rate limiting per client IP
- In-memory caching with time-to-live (TTL)
- Production deployment using Gunicorn and Render
- Secure environment variable handling
- Ready for Swagger / OpenAPI documentation


#ARCHITECTURE OVERVIEW
---------------------

Client (Postman / Swagger UI / Frontend)
        |
        v
Flask API (/jobs endpoint)
        |
        v
Authentication → Rate Limiting → Cache
        |
        v
JSearch Service (RapidAPI)
        |
        v
Normalized Job Response


#DESIGN PRINCIPLE
----------------
Routes never communicate directly with external APIs.
All third-party access is handled in the service layer.


#PROJECT STRUCTURE
-----------------

jobsearch/
- app.py
- config.py
- routes/
  - health.py
  - jobs.py
- services/
  - jsearch.py
- utils/
  - auth.py
  - cache.py
  - normalizer.py
  - rate_limiter.py
- requirements.txt
- README.txt


#AUTHENTICATION
--------------

All protected endpoints require an API key.

Request header:
X-API-Key: test-key-123

If the API key is missing or invalid, the API returns:
401 Unauthorized


#API ENDPOINTS
-------------

#Health Check
------------
Endpoint:
GET /

Response:
status: API alive


#Job Search
----------
Endpoint:
GET /jobs

Required query parameter:
- query: job title or keyword

Optional query parameters:
- country: country code (default: us)
- page: page number (default: 1)
- remote: true or false
- type: FULLTIME or CONTRACT

Required request header:
X-API-Key: your-api-key


#EXAMPLE REQUEST
---------------

GET /jobs?query=developer&remote=true


EXAMPLE RESPONSE
----------------

cached: false
page: 1
count: 10
results:
- id: XacHlAyDYl96t7ASAAAAAA==
  title: Backend Software Developer
  company: Aperio Global
  location: Washington
  remote: false
  employment_type: Full-time
  apply_link: https://www.ziprecruiter.com/...
  apply_source: ZipRecruiter
  apply_type: redirect


#APPLY LINK RESOLUTION LOGIC
---------------------------

The API selects the best available apply URL using this priority order:

1. Direct apply link from the job source
2. Google Jobs redirect link
3. Employer’s official website

If no valid link exists, apply_link is returned as null.
This reflects upstream data limitations and is expected behavior.


#CACHING
-------

- In-memory caching with a 5-minute TTL
- Cache keys include search query and filters
- Reduces repeated calls to external APIs
- Improves response performance

Cached responses include:
cached: true


#RATE LIMITING
-------------

- Maximum 20 requests per minute per IP address
- Enforced before cache and external API calls
- Exceeded limits return:
429 Too Many Requests


#ENVIRONMENT VARIABLES
---------------------

The following environment variables are required:

RAPIDAPI_KEY = your RapidAPI key
RAPIDAPI_HOST = jsearch.p.rapidapi.com

Secrets are never committed to version control.


#DEPLOYMENT
----------

- Hosted on Render
- Production server uses Gunicorn
- Automatic redeployment on push to main branch

Live API URL:
https://find-job-api.onrender.com


#TESTING
-------

- Local testing using Flask development server
- API testing using Postman
- Production testing using live Render deployment


#DESIGN DECISIONS
----------------

- Flask chosen for simplicity and explicit control
- API key authentication preferred over JWT for lightweight access
- In-memory caching used for MVP with Redis-ready design
- Strict separation of concerns across routes, services, and utilities


#FUTURE IMPROVEMENTS
-------------------

- Redis-based caching and rate limiting
- Database-backed API key management
- Salary normalization
- Job posting timestamps
- Company logos
- Frontend client application
- Advanced monitoring and analytics


#LICENSE
-------

This project is intended for educational and portfolio purposes.