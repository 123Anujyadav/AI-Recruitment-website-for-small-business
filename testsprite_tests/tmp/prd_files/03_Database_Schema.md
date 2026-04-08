# Database Schema (Minimal Design)

## User

-   id
-   email
-   password
-   role (candidate / employer)

## CandidateProfile

-   user (FK)
-   skills (JSON/Text)
-   experience
-   pincode

## EmployerProfile

-   user (FK)
-   company_name
-   pincode

## Job

-   employer (FK)
-   title
-   required_skills
-   pincode
-   created_at

## Application

-   candidate (FK)
-   job (FK)
-   match_score (float)
-   status (Applied / Shortlisted / Rejected)
