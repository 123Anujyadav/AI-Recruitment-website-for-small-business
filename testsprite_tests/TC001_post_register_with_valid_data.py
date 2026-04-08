import requests

BASE_URL = "http://localhost:8000"
REGISTER_ENDPOINT = f"{BASE_URL}/api/register"
TIMEOUT = 30


def test_post_register_with_valid_data():
    candidate_data = {
        "role": "candidate",
        "email": "candidate_test123@example.com",
        "password": "StrongPassword!23",
        "first_name": "Test",
        "last_name": "Candidate",
        "skills": ["Python", "Django", "REST"],
        "pincode": "560001"
    }

    employer_data = {
        "role": "employer",
        "email": "employer_test123@example.com",
        "password": "StrongPassword!23",
        "company_name": "TestCorp",
        "contact_person": "John Employer",
        "phone": "1234567890",
        "pincode": "560001"
    }

    created_user_ids = []

    try:
        # Register candidate user
        resp_candidate = requests.post(REGISTER_ENDPOINT, json=candidate_data, timeout=TIMEOUT)
        assert resp_candidate.status_code == 201, f"Expected 201 Created for candidate registration, got {resp_candidate.status_code}"
        candidate_resp_json = resp_candidate.json()
        assert "id" in candidate_resp_json, "Response missing user id for candidate registration"
        created_user_ids.append(("candidate", candidate_resp_json["id"]))

        # Register employer user
        resp_employer = requests.post(REGISTER_ENDPOINT, json=employer_data, timeout=TIMEOUT)
        assert resp_employer.status_code == 201, f"Expected 201 Created for employer registration, got {resp_employer.status_code}"
        employer_resp_json = resp_employer.json()
        assert "id" in employer_resp_json, "Response missing user id for employer registration"
        created_user_ids.append(("employer", employer_resp_json["id"]))

    finally:
        # Cleanup: if API offered a delete user endpoint, we would delete users here.
        # As no delete endpoint is described, skipping deletion.
        pass


test_post_register_with_valid_data()