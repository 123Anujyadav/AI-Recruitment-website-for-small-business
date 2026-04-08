import requests


BASE_URL = "http://localhost:8000"
TIMEOUT = 30


def test_get_candidate_matched_jobs_with_valid_session():
    session = requests.Session()
    candidate_email = "test_candidate_tc008@example.com"
    candidate_password = "TestPass123!"

    try:
        # Register candidate
        register_resp = session.post(
            f"{BASE_URL}/api/register",
            json={
                "role": "candidate",
                "email": candidate_email,
                "password": candidate_password
            },
            timeout=TIMEOUT,
        )
        # If already registered, ignore error 400 with proper message
        if register_resp.status_code not in (201, 400):
            register_resp.raise_for_status()
        elif register_resp.status_code == 400:
            # If error is because already registered, ignore to proceed; else fail
            error_detail = register_resp.json()
            if "email" not in str(error_detail).lower():
                raise AssertionError(f"Unexpected registration failure: {error_detail}")

        # Login candidate
        login_resp = session.post(
            f"{BASE_URL}/api/login",
            json={"email": candidate_email, "password": candidate_password},
            timeout=TIMEOUT,
        )
        assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"

        # GET matched jobs
        matched_jobs_resp = session.get(
            f"{BASE_URL}/api/candidate/matched-jobs",
            timeout=TIMEOUT,
        )
        assert matched_jobs_resp.status_code == 200, f"Expected 200 OK, got {matched_jobs_resp.status_code}"
        matched_jobs = matched_jobs_resp.json()
        assert isinstance(matched_jobs, list), "Matched jobs response is not a list"

    finally:
        # Logout candidate to clean up session
        try:
            session.post(f"{BASE_URL}/api/logout", timeout=TIMEOUT)
        except Exception:
            pass


test_get_candidate_matched_jobs_with_valid_session()