import requests
import time

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_put_employer_job_edit_with_owner_session():
    unique_suffix = str(int(time.time() * 1000))
    # Employer registration data with unique email
    employer_register_data = {
        "role": "employer",
        "email": f"owner_employer_tc007_{unique_suffix}@example.com",
        "password": "StrongPass!234"
    }
    # Employer login credentials
    employer_login_data = {
        "email": employer_register_data["email"],
        "password": employer_register_data["password"]
    }
    # Job creation data
    job_post_data = {
        "title": "Original Job Title TC007",
        "required_skills": ["Python", "Django"],
        "pincode": "560001",
        "is_walk_in": False,
        "walk_in_address": ""
    }
    # Updated job fields for PUT
    job_update_data = {
        "title": "Updated Job Title TC007",
        "required_skills": ["Python", "Django", "REST"],
        "pincode": "560002",
        "is_walk_in": True,
        "walk_in_address": "123 Updated Walk-In Address"
    }

    session = requests.Session()
    try:
        # Register employer
        resp = session.post(f"{BASE_URL}/api/register", json=employer_register_data, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Registration failed: {resp.text}"

        # Login employer
        resp = session.post(f"{BASE_URL}/api/login", json=employer_login_data, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Login failed: {resp.text}"

        # Confirm session cookie is set
        assert resp.cookies, "No session cookie set on login"

        # Create a new job
        resp = session.post(f"{BASE_URL}/api/employer/job", json=job_post_data, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Job creation failed: {resp.text}"
        job_id = resp.json().get("id")
        assert job_id is not None, "Job ID not returned on job creation"

        # PUT to update job owned by employer
        resp = session.put(f"{BASE_URL}/api/employer/job/{job_id}/edit", json=job_update_data, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Job update failed: {resp.text}"

        updated_job = resp.json()
        # Validate updated fields
        assert updated_job.get("title") == job_update_data["title"], "Title not updated correctly"
        assert updated_job.get("required_skills") == job_update_data["required_skills"], "Required skills not updated correctly"
        assert updated_job.get("pincode") == job_update_data["pincode"], "Pincode not updated correctly"
        assert updated_job.get("is_walk_in") == job_update_data["is_walk_in"], "Is_walk_in not updated correctly"
        assert updated_job.get("walk_in_address") == job_update_data["walk_in_address"], "Walk-in address not updated correctly"

    finally:
        # Cleanup: delete the job if created
        if 'job_id' in locals():
            session.delete(f"{BASE_URL}/api/employer/job/{job_id}/edit", timeout=TIMEOUT)
        # Logout employer to clean session
        session.post(f"{BASE_URL}/api/logout", timeout=TIMEOUT)
        session.close()

test_put_employer_job_edit_with_owner_session()