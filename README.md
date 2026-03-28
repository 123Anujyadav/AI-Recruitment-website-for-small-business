# TalentAI MVP — AI-Powered Job Matching System

[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-red?logo=djangorestframework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)

A full-stack job matching platform built with **Django REST Framework** and **Vanilla JS** SPA frontends. Candidates build profiles and apply to jobs; employers post listings and view applicants ranked by a computed match score. Includes AI-powered salary assessments and learning paths via Google Gemini.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Django 6, DRF |
| Frontend | Vanilla HTML/CSS/JS (SPA) |
| AI Engine | Google Gemini 2.5 Flash |
| Database | PostgreSQL + psycopg2-binary |
| CORS | django-cors-headers |
| Auth | Django session-based |

---

## Project Structure

```
TalentAI_MVP/
├── .env, .gitignore, manage.py, requirements.txt
├── install.bat, run.bat          # Windows one-click scripts
├── core/                         # Django project config (settings, urls, wsgi, asgi)
├── jobs/                         # Main app (models, views, serializers, urls, ai_services)
│   ├── admin_views.py, admin_urls.py  # Admin panel API
│   └── migrations/               # 6 migrations
├── templates/
│   ├── index.html                # Main SPA (1435 lines)
│   └── admin.html                # Admin panel SPA (833 lines)
└── venv/                         # Virtual environment (gitignored)
```

---

## Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+** running locally

---

## Setup

### Windows (one-click)
```bat
.\install.bat    # Create venv, install deps, run migrations
.\run.bat        # Start server + open browser
```

### Manual
```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
# CREATE DATABASE talentai_db;  (in PostgreSQL)
python manage.py makemigrations jobs && python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000** (main app) or **http://127.0.0.1:8000/admin-panel/** (admin).

---

## Configuration

Create a `.env` file in the project root:

```env
DJANGO_SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
DB_NAME=talentai_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | *(insecure fallback)* | Django secret key |
| `GEMINI_API_KEY` | `""` | Gemini API key for AI features |
| `DB_NAME` | `talentai_db` | PostgreSQL database |
| `DB_USER` | `postgres` | PostgreSQL user |
| `DB_PASSWORD` | `24816` | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |

**Key settings:** Custom user model `jobs.User`, CORS allow all origins, session expires on browser close (1-hour cookie).

---

## API Endpoints

### Public (`/api/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register (username, email, password, role) |
| POST | `/login` | Session login |
| POST | `/logout` | Session logout |
| GET | `/whoami` | Current user info (or 401) |
| GET | `/jobs/feed` | All jobs, newest first |

### Candidate (`/api/candidate/`) — requires `candidate` role

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/profile` | View/update profile |
| GET | `/matched-jobs` | All available jobs |
| POST | `/apply` | Apply to job (auto-computes match score) |
| GET | `/applications` | Applied jobs with HR contact info |
| GET | `/job/{id}/salary-check` | AI salary assessment |
| POST | `/job/{id}/learning-path` | AI skill gap roadmap |

### Employer (`/api/employer/`) — requires `employer` role

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/profile` | View/update company profile |
| GET/POST | `/job`, `/jobs` | List/post jobs |
| GET | `/job/{id}/ranked-candidates` | Applicants ranked by match score |
| PATCH | `/application/{id}/status` | Shortlist/Reject |
| GET/PATCH | `/job/{id}/edit` | Edit job posting |

### Admin (`/admin-panel/api/`) — requires `is_staff`

Full CRUD for users, jobs, applications, candidate profiles, employer profiles. Plus login/logout, session check, and platform stats.

---

## Matching Algorithm

When a candidate applies, a score (0-100) is computed:

```
score = (matched_skills / total_required_skills) × 70 + location_bonus × 30
```

- **Skill Overlap (70%)** — case-insensitive, comma-separated skill matching
- **Location Bonus (30%)** — full points if candidate and job pincode match
- **Pincode Priority** — same-pincode candidates always rank above out-of-pincode candidates

---

## AI Integration (Google Gemini 2.5 Flash)

| Feature | Endpoint | Output |
|---------|----------|--------|
| Salary Assessment | `GET /api/candidate/job/{id}/salary-check` | `{status, market_range, explanation}` |
| Learning Path | `POST /api/candidate/job/{id}/learning-path` | `{gap_analysis, roadmap: [{topic, focus_area, estimated_time, resource_suggestion}]}` |

Requires a valid `GEMINI_API_KEY` in `.env`.

---

## Demo Flow

1. Register as **Employer** → complete company profile
2. **Post a Job** with required skills, pincode, salary
3. Register as **Candidate** → fill in skills, experience, pincode
4. Browse the **Job Feed** → apply to a job
5. View **AI Salary Assessment** and **Learning Path**
6. Log in as Employer → view **Ranked Candidates** → Shortlist/Reject

---