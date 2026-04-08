import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_candidate_job_salary_check_with_valid_session():
    session = requests.Session()
    candidate_email = f"test_candidate_{uuid.uuid4()}@example.com"
    candidate_password = "TestPass123!"
    job_id = None

    try:
        # Register candidate
        register_payload = {
            "role": "candidate",
            "email": candidate_email,
            "password": candidate_password
        }
        r = session.post(f"{BASE_URL}/api/register", json=register_payload, timeout=TIMEOUT)
        assert r.status_code == 201, f"Registration failed: {r.status_code} {r.text}"

        # Login candidate to get session cookie
        login_payload = {
            "email": candidate_email,
            "password": candidate_password
        }
        r = session.post(f"{BASE_URL}/api/login", json=login_payload, timeout=TIMEOUT)
        assert r.status_code == 200, f"Login failed: {r.status_code} {r.text}"
        # Session cookies are automatically handled by session object

        # Get candidate profile (to ensure profile created and get pincode if needed)
        r = session.get(f"{BASE_URL}/api/candidate/profile", timeout=TIMEOUT)
        assert r.status_code == 200, f"Get candidate profile failed: {r.status_code} {r.text}"

        # Get matched jobs to obtain an existing job_id for salary check
        r = session.get(f"{BASE_URL}/api/candidate/matched-jobs", timeout=TIMEOUT)
        assert r.status_code == 200, f"Get matched jobs failed: {r.status_code} {r.text}"
        matched_jobs = r.json()
        if not matched_jobs:
            raise AssertionError("No matched jobs found for candidate to test salary check")

        job_id = matched_jobs[0].get("id") or matched_jobs[0].get("job_id")
        assert job_id is not None, "Job ID not found in matched jobs response"

        # Make salary-check request
        r = session.get(f"{BASE_URL}/api/candidate/job/{job_id}/salary-check", timeout=TIMEOUT)
        assert r.status_code == 200, f"Salary check failed: {r.status_code} {r.text}"

        data = r.json()
        assert "salary_assessment" in data or "salaryAssessment" in data or "assessment" in data, "Missing salary assessment in response"
        assert "rationale" in data or "explanation" in data or "reasoning" in data, "Missing rationale in response"

    finally:
        # Logout candidate to cleanup session
        try:
            session.post(f"{BASE_URL}/api/logout", timeout=TIMEOUT)
        except:
            pass

test_get_candidate_job_salary_check_with_valid_session()