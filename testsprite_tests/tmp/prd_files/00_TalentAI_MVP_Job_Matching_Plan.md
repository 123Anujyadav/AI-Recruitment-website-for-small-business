# TalentAI MVP Plan

## Simple Job Matching & Candidate Ranking System

------------------------------------------------------------------------

## 1. Objective

Build a **simple recruitment system** that performs:

-   Candidate Registration & Profile Creation
-   Job Posting by Employer
-   Skill-Based Job Matching
-   Candidate Ranking based on Match Score

No advanced AI, no embeddings, no salary prediction, no analytics.

------------------------------------------------------------------------

## 2. MVP Scope (Only Core Features)

### Candidate Module

-   Register / Login
-   Create Profile (Skills, Experience, Pincode)
-   Upload Resume (Optional -- text extraction only)
-   View Matched Jobs
-   Apply to Jobs

### Employer Module

-   Register / Login
-   Post Job (Title, Required Skills, Pincode)
-   View Ranked Candidates for Each Job
-   Update Application Status

------------------------------------------------------------------------

## 3. System Architecture (Simple)

### Backend

-   Django
-   Django REST Framework
-   PostgreSQL

### Frontend

-   HTML
-   CSS
-   JavaScript (Fetch API)

No pgvector, no ML pipelines.

------------------------------------------------------------------------

## 4. Database Design (Minimal)

### User

-   id
-   email
-   password
-   role (candidate / employer)

### CandidateProfile

-   user (FK)
-   skills (JSONField or TextField)
-   experience
-   pincode

### EmployerProfile

-   user (FK)
-   company_name
-   pincode

### Job

-   employer (FK)
-   title
-   required_skills (JSONField or TextField)
-   pincode
-   created_at

### Application

-   candidate (FK)
-   job (FK)
-   match_score (FloatField)
-   status (Applied / Shortlisted / Rejected)

------------------------------------------------------------------------

## 5. Matching Logic (Simple Formula)

### Step 1: Skill Matching

matched_skills = number of common skills\
total_required_skills = total skills in job

skill_score = (matched_skills / total_required_skills) \* 70

### Step 2: Location Matching

If candidate_pincode == job_pincode:\
location_score = 30\
Else:\
location_score = 0

### Step 3: Final Score

total_score = skill_score + location_score

------------------------------------------------------------------------

## 6. Candidate Ranking

For each job:

1.  Calculate match_score for every candidate.
2.  Store score in Application table.
3.  Sort candidates by match_score (descending).
4.  Return ranked list to employer.

------------------------------------------------------------------------

## 7. Development Plan

### Phase 1 -- Setup (3 Days)

-   Setup Django Project
-   Create Models
-   Setup Authentication

### Phase 2 -- Job & Profile APIs (4 Days)

-   Candidate Profile API
-   Job Posting API
-   Application API

### Phase 3 -- Matching Engine (3 Days)

-   Implement skill comparison logic
-   Implement ranking endpoint

### Phase 4 -- Basic Frontend (5 Days)

-   Login/Register Page
-   Dashboard
-   Job Posting Form
-   Ranked Candidate View

------------------------------------------------------------------------

## 8. Expected Outcome

-   Employer posts a job
-   Candidates apply
-   System calculates match score
-   Employer sees ranked candidate list

This completes a functional MVP focused only on Job Matching and
Candidate Ranking.
