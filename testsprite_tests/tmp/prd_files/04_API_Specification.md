# API Specification

## Authentication

POST /api/register POST /api/login

## Candidate

GET /api/candidate/profile POST /api/candidate/profile GET
/api/candidate/matched-jobs POST /api/candidate/apply

## Employer

POST /api/employer/job GET /api/employer/jobs GET
/api/employer/job/{id}/ranked-candidates PATCH
/api/employer/application/{id}/status
