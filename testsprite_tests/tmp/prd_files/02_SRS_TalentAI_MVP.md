# Software Requirement Specification (SRS)

## 1. Functional Requirements

FR1: Users must be able to register and login. FR2: Candidates must
create profiles with skills & pincode. FR3: Employers must post jobs
with required skills. FR4: System must calculate match_score
automatically. FR5: Employer must see ranked candidate list.

## 2. Non-Functional Requirements

-   Response time \< 2 seconds for ranking
-   Secure authentication
-   Scalable database structure

## 3. Constraints

-   No ML pipeline
-   PostgreSQL only
-   Django REST backend
