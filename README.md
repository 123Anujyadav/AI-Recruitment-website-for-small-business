# TalentAI MVP — AI-Powered Job Matching System

[![Django](https://img.shields.io/badge/Django-6.0-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-red?logo=djangorestframework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-stack AI-powered recruitment platform that matches candidates to jobs using a proprietary skill-overlap + geo-location algorithm, with Generative AI career tools powered by Google Gemini.

> **Candidates** build profiles, browse jobs, apply with instant match scoring, and get AI-powered salary assessments & personalized learning paths.  
> **Employers** post listings, view applicants auto-ranked by match score, and manage the hiring pipeline.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart Match Scoring** | Proprietary 0–100 score combining skill overlap (70%) and pincode proximity (30%) |
| 🤖 **AI Salary Assessment** | Gemini-powered real-time salary evaluation against market standards |
| 📚 **AI Learning Paths** | Personalized skill-gap roadmaps generated for each job listing |
| 📍 **Hyper-Local Ranking** | Pincode-aware sorting that organically boosts local talent |
| 🏢 **Employer Dashboard** | Auto-ranked applicant lists with shortlist/reject workflow |
| 🚶 **Walk-In Support** | Native walk-in job type with physical address handling |
| 🔐 **Session-Based Auth** | Secure Django session auth with role-based access (Candidate / Employer / Admin) |
| 📱 **SPA Frontend** | Smooth single-page experience built with vanilla JS — no framework bloat |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Django 6, Django REST Framework |
| Frontend | Vanilla HTML5 / CSS3 / JavaScript (SPA architecture) |
| AI Engine | Google Gemini 2.5 Flash |
| Database | PostgreSQL 14+ with psycopg2-binary |
| CORS | django-cors-headers |
| Auth | Django session-based with custom User model |
| Env Config | python-dotenv |

---

## 📁 Project Structure

```
TalentAI_MVP/
├── .env.example              # Environment template (copy to .env)
├── .gitignore
├── manage.py
├── requirements.txt
├── install.bat               # Windows: one-click setup
├── run.bat                   # Windows: start server + open browser
│
├── core/                     # Django project configuration
│   ├── settings.py           # Settings (DB, auth, CORS, Gemini key)
│   ├── urls.py               # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── jobs/                     # Main application
│   ├── models.py             # User, CandidateProfile, EmployerProfile, Job, Application
│   ├── views.py              # Public, Candidate, and Employer API views
│   ├── serializers.py        # DRF serializers
│   ├── urls.py               # API route definitions
│   ├── ai_services.py        # Gemini AI integration (salary check, learning paths)
│   ├── admin_views.py        # Admin panel API views
│   ├── admin_urls.py         # Admin panel routes
│   └── migrations/           # 12 database migrations
│
├── templates/
│   ├── index.html            # Main SPA frontend
│   └── admin.html            # Admin panel SPA
│
└── static/
    ├── css/                  # index.css, admin.css
    ├── js/                   # index.js, admin.js
    └── img/                  # Static assets (avatar.png)
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **PostgreSQL 14+** — [Download](https://www.postgresql.org/download/)
- **Git** — [Download](https://git-scm.com/downloads)

### 1. Clone the Repository

```bash
git clone https://github.com/Anujyadav123/TalentAI_MVP.git
cd TalentAI_MVP
```


### 2. Set Up Environment Variables

```bash
# Copy the example file and fill in your values
cp .env.example .env
```

Open `.env` and update:

```env
DJANGO_SECRET_KEY=your-django-secret-key
GEMINI_API_KEY=your-google-gemini-api-key
DB_NAME=talentai_db
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

> **💡 Tip:** Get a free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey). The app works without it, but AI features (salary check & learning paths) will be disabled.

### 3. Create the Database

Open PostgreSQL shell or pgAdmin and run:

```sql
CREATE DATABASE talentai_db;
```

### 4. Install & Run

#### Windows (One-Click)

```bat
.\install.bat        # Creates venv, installs dependencies, runs migrations
.\run.bat            # Starts server and opens browser automatically
```

#### Manual Setup (Windows / macOS / Linux)

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations jobs
python manage.py migrate

# Start the server
python manage.py runserver
```

### 5. Open the App

| Page | URL |
|------|-----|
| **Main App** | [http://127.0.0.1:8000](http://127.0.0.1:8000) |
| **Admin Panel** | [http://127.0.0.1:8000/admin-panel/](http://127.0.0.1:8000/admin-panel/) |

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | *(insecure fallback)* | Django secret key for cryptographic signing |
| `GEMINI_API_KEY` | `""` | Google Gemini API key for AI features |
| `DB_NAME` | `talentai_db` | PostgreSQL database name |
| `DB_USER` | `postgres` | PostgreSQL username |
| `DB_PASSWORD` | — | PostgreSQL password |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |

**Notable settings:** Custom user model (`jobs.User`), CORS allow all origins (dev mode), session expires on browser close with 1-hour cookie age.

---

## 📡 API Reference

### Public Endpoints — `/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/register` | Register (username, email, password, role) |
| `POST` | `/api/login` | Session login |
| `POST` | `/api/logout` | Session logout |
| `GET` | `/api/whoami` | Current authenticated user info |
| `GET` | `/api/jobs/feed` | All active jobs, newest first |

### Candidate Endpoints — `/api/candidate/` *(requires `candidate` role)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET / POST` | `/api/candidate/profile` | View / update candidate profile |
| `GET` | `/api/candidate/matched-jobs` | Browse all available jobs |
| `POST` | `/api/candidate/apply` | Apply to a job (auto-calculates match score) |
| `GET` | `/api/candidate/applications` | View applied jobs with HR contact info |
| `GET` | `/api/candidate/job/{id}/salary-check` | AI salary assessment for a job |
| `POST` | `/api/candidate/job/{id}/learning-path` | AI-generated skill-gap roadmap |

### Employer Endpoints — `/api/employer/` *(requires `employer` role)*

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET / POST` | `/api/employer/profile` | View / update company profile |
| `GET / POST` | `/api/employer/job`, `/api/employer/jobs` | List / post jobs |
| `GET` | `/api/employer/job/{id}/ranked-candidates` | Applicants ranked by match score |
| `PATCH` | `/api/employer/application/{id}/status` | Shortlist or reject applicant |
| `GET / PATCH` | `/api/employer/job/{id}/edit` | View / edit job posting |

### Admin Endpoints — `/admin-panel/api/` *(requires `is_staff`)*

Full CRUD for users, jobs, applications, candidate profiles, and employer profiles. Includes platform stats, login/logout, and session management.

---

## 🧮 Matching Algorithm

When a candidate applies, a **Match Score (0–100)** is computed in real-time:

```
Match Score = (matched_skills / total_required_skills) × 70  +  location_bonus × 30
```

| Component | Weight | Logic |
|-----------|--------|-------|
| **Skill Overlap** | 70% | Case-insensitive comparison of candidate skills vs. job requirements |
| **Location Bonus** | 30% | Full points if candidate's 6-digit pincode matches the job's pincode |
| **Ranking Rule** | — | Same-pincode candidates always rank above out-of-pincode candidates |

---

## 🤖 AI Integration — Google Gemini 2.5 Flash

| Feature | Endpoint | Response |
|---------|----------|----------|
| **Salary Assessment** | `GET /api/candidate/job/{id}/salary-check` | `{status, market_range, explanation}` |
| **Learning Path** | `POST /api/candidate/job/{id}/learning-path` | `{gap_analysis, roadmap: [{topic, focus_area, estimated_time, resource_suggestion}]}` |

> Requires a valid `GEMINI_API_KEY` in your `.env` file.

---

## 🎮 Demo Walkthrough

1. **Register as Employer** → Complete company profile (name, pincode, HR contact)
2. **Post a Job** → Add title, required skills, pincode, salary, optional walk-in details
3. **Register as Candidate** → Fill in skills, experience, pincode, contact info
4. **Browse the Job Feed** → View all available postings
5. **Apply to a Job** → Match score is instantly calculated and saved
6. **AI Salary Check** → Get a market salary assessment for any job
7. **AI Learning Path** → Get a personalized roadmap to bridge skill gaps
8. **Login as Employer** → View ranked candidates → Shortlist or Reject
9. **Admin Panel** → Manage all users, jobs, and applications with full CRUD access

---

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center">
  Built with ❤️ using Django, DRF & Google Gemini
</p>
