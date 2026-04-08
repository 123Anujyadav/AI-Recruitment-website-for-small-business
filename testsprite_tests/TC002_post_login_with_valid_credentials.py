import requests

BASE_URL = "http://localhost:8000"


def test_post_login_with_valid_credentials():
    # Prepare valid candidate registration data
    register_url = f"{BASE_URL}/api/register"
    login_url = f"{BASE_URL}/api/login"

    candidate_data = {
        "role": "candidate",
        "email": "testcandidate@example.com",
        "password": "StrongPass123!"
    }

    try:
        # Register new candidate user
        r_register = requests.post(register_url, json=candidate_data, timeout=30)
        assert r_register.status_code == 201, f"Registration failed: {r_register.text}"
        user_id = r_register.json().get("id")
        assert user_id is not None, "User ID missing in registration response"

        # Attempt login with valid credentials
        login_payload = {
            "email": candidate_data["email"],
            "password": candidate_data["password"]
        }
        r_login = requests.post(login_url, json=login_payload, timeout=30)
        assert r_login.status_code == 200, f"Login failed: {r_login.text}"

        # Verify session cookie is set
        cookies = r_login.cookies
        session_cookie = cookies.get_dict()
        assert session_cookie, "Session cookie missing after login"
    finally:
        if 'user_id' in locals():
            # Attempt cleanup: no explicit delete user endpoint mentioned,
            # so this may be a noop or you can add administrative cleanup if available
            pass


test_post_login_with_valid_credentials()