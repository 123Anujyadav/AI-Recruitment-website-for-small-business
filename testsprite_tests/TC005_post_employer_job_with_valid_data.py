import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_employer_job_with_valid_data():
    session = requests.Session()
    unique_email = f"employer_{uuid.uuid4()}@example.com"
    try:
        # Step 0: Register employer (to ensure account exists)
        register_url = f"{BASE_URL}/api/register"
        employer_registration = {
            "role": "employer",
            "email": unique_email,
            "password": "StrongPassword123!"
        }
        register_resp = session.post(register_url, json=employer_registration, timeout=TIMEOUT)
        # Allow 201 Created or 400 Bad Request if already registered
        assert register_resp.status_code in (201, 400), f"Registration failed: {register_resp.text}"

        # Step 1: Login as employer to get session cookie
        login_url = f"{BASE_URL}/api/login"
        employer_credentials = {
            "email": unique_email,
            "password": "StrongPassword123!"
        }
        login_resp = session.post(login_url, json=employer_credentials, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"

        # Step 2: Post a new job with valid data
        post_job_url = f"{BASE_URL}/api/employer/job"
        job_data = {
            "title": "Senior Software Engineer",
            "required_skills": ["Python", "Django", "REST"],
            "pincode": "123456",
            "is_walk_in": False,
            "walk_in_address": ""
        }
        post_job_resp = session.post(post_job_url, json=job_data, timeout=TIMEOUT)
        assert post_job_resp.status_code == 201, f"Job creation failed: {post_job_resp.text}"
        response_json = post_job_resp.json()
        assert "id" in response_json, "Response missing job id"
        job_id = response_json["id"]
    finally:
        # Cleanup: delete the job if created
        if 'job_id' in locals():
            delete_url = f"{BASE_URL}/api/employer/job/{job_id}/edit"
            # No delete endpoint specified, skip cleanup
            pass

test_post_employer_job_with_valid_data()