# Find Job API

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Angular](https://img.shields.io/badge/Frontend-Angular-DD0031?style=flat-square&logo=angular&logoColor=white)
![SQLite](https://img.shields.io/badge/Auth%20Store-SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

Production-style full-stack job search app built with Flask and Angular.

It combines multiple provider APIs behind one normalized backend contract, then layers on account creation, API-key auth, protected frontend routes, saved jobs, personal notes, and search activity tracking.

## Why This Repo Exists

Job APIs rarely agree on request shapes, field names, auth requirements, or filtering behavior. This project smooths that out with a single `/api/jobs` interface and a frontend that feels like one product instead of a collection of provider integrations.

## Highlights

- Unified job search API across multiple providers
- Country-based engine routing with normalized job payloads
- Account registration and login with SQLite-backed user records
- Rotating API keys stored as salted hashes, not plain text
- Protected Angular routes for search, saved roles, activity, and job detail views
- Browser-persisted saved jobs, notes, and recent search history
- Swagger UI for interactive API testing
- Runtime fallback to sample jobs when live provider calls fail
- Production-style deployment path where Flask can serve the built Angular app

## Supported Provider Flow

- `us` and most non-UK countries: RapidAPI JSearch
- `uk` / `gb`: Adzuna
- Response shape returned to clients: normalized into one consistent schema

> Runtime fallback is available when a provider request fails, but the backend still requires valid RapidAPI configuration at startup because the JSearch engine is imported during app boot.

## Architecture

```text
Angular SPA
  |- Login / Register
  |- Search / Saved / Activity / Role Detail
  |- localStorage for session, notes, and search history
  v
Flask API
  |- /api/auth/register
  |- /api/auth/login
  |- /api/jobs
  |- /api/health
  |- /apidocs
  v
Service Layer
  |- engine_factory.py
  |- user_store.py
  v
Provider Engines
  |- JSearch
  |- Adzuna
```

## Tech Stack

| Layer | Tools | Responsibility |
| --- | --- | --- |
| Backend | Flask, Requests, Flasgger | REST API, provider orchestration, docs |
| Frontend | Angular 21, RxJS | Auth flow, search UX, saved-job workflows |
| Persistence | SQLite, browser `localStorage` | User accounts, session state, notes, history |
| Auth | API keys, salted SHA-256 hashes | Protected access to job search endpoints |
| Docs | Swagger UI | Interactive exploration of the API |

## Local Development

### Prerequisites

- Python 3.11 or newer recommended
- Node.js LTS recommended
- npm

Angular CLI 21 works best on an LTS Node release. Avoid Node 25 for local Angular development.

### 1. Clone the Repository

```bash
git clone https://github.com/parthrohit22/find-job-api.git
cd find-job-api
```

### 2. Set Up the Backend

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set Up the Frontend

```bash
cd frontend
npm install
cd ..
```

### 4. Configure Environment Variables

Create a root `.env` file:

```env
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=jsearch.p.rapidapi.com
ADZUNA_APP_ID=your_adzuna_app_id
ADZUNA_APP_KEY=your_adzuna_app_key
APP_PORT=5001
USER_DB_PATH=data/jobsearch.sqlite3
```

| Variable | Required | Purpose |
| --- | --- | --- |
| `RAPIDAPI_KEY` | Yes | Required for backend startup and JSearch requests |
| `RAPIDAPI_HOST` | Yes | RapidAPI host, typically `jsearch.p.rapidapi.com` |
| `ADZUNA_APP_ID` | Only for live UK/GB searches | Adzuna application ID |
| `ADZUNA_APP_KEY` | Only for live UK/GB searches | Adzuna application key |
| `APP_PORT` | No | Flask port, defaults to `5001` |
| `USER_DB_PATH` | No | SQLite database path, defaults to `data/jobsearch.sqlite3` |

Never commit `.env` files or real credentials.

### 5. Start the App in Development Mode

Run the backend in one terminal:

```bash
source venv/bin/activate
python app.py
```

Run the Angular frontend in another terminal:

```bash
cd frontend
npm start
```

Open:

- Frontend: `http://localhost:4200`
- Backend API: `http://127.0.0.1:5001`
- Swagger UI: `http://127.0.0.1:5001/apidocs`

The Angular dev server proxies `/api` requests to Flask through [`frontend/proxy.conf.json`](frontend/proxy.conf.json).

## Production-Style Local Run

Build the Angular app:

```bash
cd frontend
npm run build
cd ..
```

Then start Flask:

```bash
source venv/bin/activate
python app.py
```

If the frontend build exists, Flask serves the compiled SPA from `frontend/dist/frontend/browser`.

## API Overview

### Auth Endpoints

| Method | Route | Description |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Create a user and issue an API key |
| `POST` | `/api/auth/login` | Authenticate a user and rotate the API key |

### Core Endpoints

| Method | Route | Description |
| --- | --- | --- |
| `GET` | `/api/jobs` | Search jobs with normalized results |
| `GET` | `/api/health` | Basic health check |
| `GET` | `/apidocs` | Swagger UI |

### `GET /api/jobs`

Required header:

```http
X-API-Key: your-api-key
```

Required query parameter:

- `query`

Optional query parameters:

- `country` default `us`
- `location`
- `distance`
- `page` default `1`
- `work_mode` one of `remote`, `hybrid`, `onsite`
- `type` such as `FULLTIME`, `PARTTIME`, `CONTRACT`, `INTERNSHIP`

Example:

```bash
curl "http://127.0.0.1:5001/api/jobs?query=backend%20engineer&country=us&location=Austin&work_mode=remote&type=FULLTIME" \
  -H "X-API-Key: your-api-key"
```

Example response:

```json
{
  "cached": false,
  "query": "backend engineer",
  "country": "us",
  "filters": {
    "location": "Austin",
    "distance": null,
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
      "remote": false,
      "work_mode": "remote",
      "employment_type": "Full-time",
      "apply_link": "https://www.example.com/apply",
      "apply_source": "Company Site",
      "apply_type": "direct"
    }
  ],
  "source": "provider",
  "warning": null
}
```

## Frontend Experience

The Angular app includes:

- Registration and sign-in flows
- Search form with country, location, distance, work mode, and type filters
- Saved jobs with inline personal notes
- Recent-search activity tracking with one-click rerun
- Role detail page backed by the latest API response or saved-job storage
- Protected routes that redirect unauthenticated users to the login screen

## Project Structure

```text
find-job-api/
├── app.py
├── config.py
├── requirements.txt
├── routes/
│   ├── auth.py
│   ├── health.py
│   └── jobs.py
├── services/
│   ├── engine_factory.py
│   ├── user_store.py
│   └── engines/
│       ├── base.py
│       ├── adzuna.py
│       └── jsearch.py
├── utils/
│   ├── auth.py
│   ├── cache.py
│   ├── normalizer.py
│   ├── rate_limiter.py
│   └── sample_jobs.py
├── data/
└── frontend/
    └── src/
```

## Implementation Notes

- User records live in SQLite, while saved jobs, notes, and search history live in browser storage.
- API keys are rotated on login and only stored server-side as salted hashes with a searchable prefix.
- Rate limiting is applied per IP address and currently defaults to `20` requests per `60` seconds.
- The job response includes a `source` field so the client can distinguish live provider data from `sample_fallback`.
- Legacy API-key login remains supported for compatibility.

## Good Next Improvements

- Add automated backend and frontend test coverage around auth, search filters, and fallback behavior
- Wire the existing cache utility into provider fetches and expose real cache metadata in responses
- Add Docker and a documented Gunicorn deployment recipe for easier deployment
- Expand provider routing beyond JSearch and Adzuna

## License

No license file is currently included in this repository.
