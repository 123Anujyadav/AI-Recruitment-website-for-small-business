# TalentAI — AI-Powered Job Matching Ecosystem

*Final Year Project Documentation*

---

## 🌟 Problem Statement

Traditional job portals suffer from two critical inefficiencies:

1. **The Black Hole Effect** — Candidates submit hundreds of applications into a void with no feedback, while HR departments are overwhelmed by thousands of unranked, often irrelevant resumes.
2. **Geographical & Skill Mismatch** — Employers struggle to find local talent (leading to high relocation friction), and candidates have no clear direction on what skills they need to develop for their targeted roles.

---

## 🚀 The TalentAI Solution

TalentAI is an intelligent, full-stack recruitment platform that bridges the gap between skilled candidates and employers using a combination of **algorithmic skill matching**, **geo-spatial ranking**, and **Generative AI career tools**.

The platform introduces an automated screening and guidance system that:
- Evaluates candidates instantly with a transparent, mathematical Match Score
- Provides employers with auto-ranked applicant lists — eliminating manual resume screening
- Offers AI-generated career guidance (salary assessments and learning paths) to help candidates grow

---

## 💡 Key Innovations & USPs

### 1. Proprietary Match Scoring Algorithm (0–100)

Every application is evaluated in real-time using a dual-factor scoring engine:

```
Match Score = (Skill Overlap × 70%) + (Location Proximity × 30%)
```

- **Skill Synergy (70%)** — Case-insensitive semantic overlap between candidate strengths and job requirements
- **Geographic Optimization (30%)** — Exact 6-digit pincode matching that organically boosts local talent
- **Fair Ranking Rule** — When skills are comparable, local candidates are strictly ranked above out-of-area applicants, reducing employer attrition and relocation costs

### 2. Applied Generative AI (Beyond Chatbots)

Unlike simple LLM wrappers, TalentAI deeply integrates **Google Gemini 2.5 Flash** for structured, domain-specific tasks:

- **Instant Salary Assessments** — Dynamically computes market-standard salary ranges with explanations based on the specific job role, requirements, and current industry trends
- **Personalized Learning Paths** — If a candidate lacks certain skills for a role, Gemini generates a structured curriculum including gap analysis, focus areas, estimated timelines, and resource suggestions

### 3. Transparent, Bias-Free Pre-Screening

The Match Score is mathematically derived from objective data (skills + pincode). Initial HR bias — such as gender, age, or ethnicity — is completely removed from the primary screening phase. **The algorithm only sees merit.**

### 4. Walk-In & Offline Integration

Acknowledging blue-collar, entry-level, and retail recruitment realities, the platform natively handles walk-in job flags and physical address logistics within the data model, bridging the online-to-offline hiring continuum.

### 5. Role-Based Multi-Panel Architecture

Three distinct interfaces serve different stakeholders:
- **Candidate Portal** — Profile management, job browsing, applications, AI tools
- **Employer Dashboard** — Job posting, ranked applicant lists, shortlist/reject workflow
- **Admin Panel** — Full CRUD management of all platform entities with stats dashboard

---

## 🛠️ System Architecture & Technology Stack

The platform follows industry-standard decoupling (Backend REST API + Frontend SPA), making it scalable and ready for future mobile application integration without backend changes.

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend / Core Engine** | Python 3.10+, Django 6 | Business logic, ORM, session auth |
| **API Layer** | Django REST Framework | RESTful API with serializers & viewsets |
| **Database** | PostgreSQL 14+ | Relational integrity, security, scalability |
| **AI Integration** | Google Gemini 2.5 Flash API | Salary assessment, learning path generation |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript | SPA architecture for seamless navigation |
| **Environment** | python-dotenv | Isolated secret management via `.env` |
| **Security** | Session auth, CORS headers, CSRF | Role-based access with session expiry |

### Data Models

| Model | Key Fields | Purpose |
|-------|------------|---------|
| `User` | username, email, role (candidate/employer) | Custom auth user extending AbstractUser |
| `CandidateProfile` | skills, experience, pincode, city, phone, about, social_links | Candidate details & contact info |
| `EmployerProfile` | company_name, pincode, city, contact_name, contact_email, org_details | Company profile & HR contact |
| `Job` | title, description, required_skills, pincode, salary, is_walk_in, expires_at | Job listing with walk-in support |
| `Application` | candidate, job, match_score, status (Applied/Shortlisted/Rejected) | Application tracking with computed score |

---

## 📊 End-to-End Workflow

```
┌─────────────┐    ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
│  Register & │───▶│  Post Jobs / │───▶│  Apply with   │───▶│  AI Career   │
│  Build      │    │  Browse Feed │    │  Auto Match   │    │  Tools       │
│  Profile    │    │              │    │  Scoring      │    │  (Gemini)    │
└─────────────┘    └──────────────┘    └───────────────┘    └──────────────┘
                                              │
                                              ▼
                                       ┌──────────────┐
                                       │  Employer    │
                                       │  Reviews     │
                                       │  Ranked List │
                                       │  ↓           │
                                       │  Shortlist / │
                                       │  Reject      │
                                       └──────────────┘
```

1. **Profile Generation** — Candidates define their skills, experience, and location (pincode). Employers establish company identity and post geo-pinpointed job listings.
2. **Algorithmic Discovery** — The system presents candidates with a ranked feed of the most relevant jobs.
3. **Application & Evaluation** — On application, the system calculates and persists the Match Score in real-time.
4. **AI Upskilling Loop** — Candidates can query the AI engine against any job listing for a personalized learning roadmap or salary fairness check.
5. **Employer Decisioning** — Employers access an ATS-style dashboard to see auto-ranked shortlists and manage application statuses (Applied → Shortlisted → Rejected).

---

## 🔌 API Surface

The platform exposes **20+ REST endpoints** across four scopes:

- **Public** (`/api/`) — Registration, login, logout, session check, job feed
- **Candidate** (`/api/candidate/`) — Profile CRUD, job matching, applications, AI salary check, AI learning paths
- **Employer** (`/api/employer/`) — Profile CRUD, job CRUD, ranked candidates, application status management
- **Admin** (`/admin-panel/api/`) — Full CRUD for all entities, platform stats, user management

---

## 🎓 Academic Contribution & Conclusion

TalentAI represents a robust, production-ready implementation of a modern recruitment ecosystem. It successfully transitions Artificial Intelligence from a novelty into a fundamental backend utility that actively solves structural employment inefficiencies.

**Key contributions:**
- **Algorithmic Fairness** — Bias-free pre-screening through mathematical scoring
- **Hyper-Local Matching** — Pincode-aware ranking that reduces relocation friction
- **AI-Enabled Mentorship** — Generative AI integrated as a career guidance tool, not just a chatbot
- **Full-Stack Architecture** — Decoupled REST API + SPA pattern ready for mobile expansion

This project bridges the gap between modern technology and socio-economic utility, demonstrating exceptional technical depth, architectural maturity, and practical real-world value.

---

> *For setup instructions and API documentation, see [README.md](README.md).*