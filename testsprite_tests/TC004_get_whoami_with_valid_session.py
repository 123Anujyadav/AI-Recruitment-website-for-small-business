import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_whoami_with_valid_session():
    register_url = f"{BASE_URL}/api/register"
    login_url = f"{BASE_URL}/api/login"
    whoami_url = f"{BASE_URL}/api/whoami"
    logout_url = f"{BASE_URL}/api/logout"

    candidate_data = {
        "role": "candidate",
        "email": "testcandidate_tc004@example.com",
        "password": "StrongPass!123"
    }

    session = requests.Session()

    try:
        # Register candidate
        resp = session.post(register_url, json=candidate_data, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Expected 201 Created for registration, got {resp.status_code}"
        user_id = resp.json().get("id")
        assert user_id is not None, "User id missing in registration response"

        # Login candidate
        login_data = {
            "email": candidate_data["email"],
            "password": candidate_data["password"]
        }
        resp = session.post(login_url, json=login_data, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Expected 200 OK for login, got {resp.status_code}"
        # Check that session cookie is set
        assert session.cookies.get_dict(), "Session cookie not set after login"

        # Get whoami with valid session
        resp = session.get(whoami_url, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Expected 200 OK for whoami, got {resp.status_code}"
        data = resp.json()
        assert "email" in data and data["email"] == candidate_data["email"], "Email mismatch in whoami response"
        assert "role" in data and data["role"] == candidate_data["role"], "Role mismatch in whoami response"
        assert "id" in data and data["id"] == user_id, "User ID mismatch in whoami response"

    finally:
        # Logout to end session
        resp = session.post(logout_url, timeout=TIMEOUT)
        assert resp.status_code == 200 or resp.status_code == 401, "Logout did not return 200 OK or 401 (if already logged out)"
        
        # Cleanup is not explicitly provided for deletion, so skipping user delete

test_get_whoami_with_valid_session()