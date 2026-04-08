import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_post_logout_with_valid_session():
    register_url = f"{BASE_URL}/api/register"
    login_url = f"{BASE_URL}/api/login"
    logout_url = f"{BASE_URL}/api/logout"

    candidate_email = "test_candidate_logout@example.com"
    candidate_password = "StrongPassw0rd!"

    # Register candidate
    register_payload = {
        "role": "candidate",
        "name": "Test Candidate",
        "email": candidate_email,
        "password": candidate_password
    }

    reg_resp = requests.post(register_url, json=register_payload, timeout=TIMEOUT)
    if reg_resp.status_code == 400:
        # Check if error is about existing email, allow test proceed
        err = reg_resp.json()
        assert "email" in err and any("already exists" in m for m in err["email"]), f"Unexpected registration failure: {reg_resp.text}"
    else:
        assert reg_resp.status_code == 201, f"Registration failed: {reg_resp.text}"

    # Login candidate
    login_payload = {
        "email": candidate_email,
        "password": candidate_password
    }
    login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    assert "set-cookie" in login_resp.headers or "Set-Cookie" in login_resp.headers, "Session cookie missing in login response"

    # Extract session cookie to use in logout
    cookies = login_resp.cookies
    assert cookies, "No cookies received in login response"

    # Perform logout with valid session cookie
    logout_resp = requests.post(logout_url, cookies=cookies, timeout=TIMEOUT)
    assert logout_resp.status_code == 200, f"Logout failed: {logout_resp.text}"

    # Verify that session cookie is no longer valid by accessing whoami endpoint
    whoami_url = f"{BASE_URL}/api/whoami"
    whoami_resp = requests.get(whoami_url, cookies=cookies, timeout=TIMEOUT)
    assert whoami_resp.status_code == 401, "Session should be invalid after logout"

    # Cleanup: attempt to login again to get session then delete user if API supported
    # Since deletion endpoint is not provided in PRD, no cleanup beyond this.


test_post_logout_with_valid_session()
