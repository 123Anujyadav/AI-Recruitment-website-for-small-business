import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_candidate_apply_with_valid_data():
    session = requests.Session()
    try:
        # 1. Register candidate
        candidate_email = "testcandidate_tc009@example.com"
        candidate_password = "SecurePass123!"
        register_payload = {
            "role": "candidate",
            "email": candidate_email,
            "password": candidate_password
        }
        resp = session.post(f"{BASE_URL}/api/register", json=register_payload, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Expected 201 Created on candidate registration, got {resp.status_code}"
        candidate_user_id = resp.json().get("id")
        assert candidate_user_id is not None, "No candidate user id returned on registration"

        # 2. Login candidate
        login_payload = {
            "email": candidate_email,
            "password": candidate_password
        }
        resp = session.post(f"{BASE_URL}/api/login", json=login_payload, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Expected 200 OK on login, got {resp.status_code}"
        assert "sessionid" in session.cookies.get_dict(), "Session cookie not set on login"

        # 3. Register employer (to create a job)
        employer_email = "testemployer_tc009@example.com"
        employer_password = "SecurePass123!"
        employer_register_payload = {
            "role": "employer",
            "email": employer_email,
            "password": employer_password
        }
        resp = requests.post(f"{BASE_URL}/api/register", json=employer_register_payload, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Expected 201 Created on employer registration, got {resp.status_code}"

        # 4. Login employer to create job
        employer_session = requests.Session()
        employer_login_payload = {
            "email": employer_email,
            "password": employer_password
        }
        resp = employer_session.post(f"{BASE_URL}/api/login", json=employer_login_payload, timeout=TIMEOUT)
        assert resp.status_code == 200, "Employers login failed"
        assert "sessionid" in employer_session.cookies.get_dict(), "Employer session cookie missing"

        # 5. Post a job as employer
        job_payload = {
            "title": "Software Engineer TC009",
            "required_skills": ["Python", "Django"],
            "pincode": "123456",
            "is_walk_in": False,
            "walk_in_address": ""
        }
        resp = employer_session.post(f"{BASE_URL}/api/employer/job", json=job_payload, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Expected 201 Created on job post, got {resp.status_code}"
        job_id = resp.json().get("id")
        assert job_id is not None, "Job id missing in job post response"

        # 6. Candidate gets or creates profile
        resp = session.get(f"{BASE_URL}/api/candidate/profile", timeout=TIMEOUT)
        assert resp.status_code == 200, "Failed to get/create candidate profile"
        profile = resp.json()
        assert profile is not None, "Candidate profile response empty"

        # 7. POST /api/candidate/apply with valid job_id and optional resume text
        apply_payload = {
            "job_id": job_id,
            "optional_resume_text": "Experienced in Python and Django development."
        }
        resp = session.post(f"{BASE_URL}/api/candidate/apply", json=apply_payload, timeout=TIMEOUT)
        assert resp.status_code in (200, 201), f"Expected 200 OK or 201 Created on apply, got {resp.status_code}"
        json_resp = resp.json()
        assert "application_id" in json_resp, "application_id missing in apply response"
        assert "match_score" in json_resp, "match_score missing in apply response"
        assert isinstance(json_resp["match_score"], (float, int)), "match_score not a number"

    finally:
        # Cleanup: delete job (if API existed to delete jobs, we would call it here)
        # Candidate and employer cleanup not specified, so skipping.
        pass

test_post_candidate_apply_with_valid_data()