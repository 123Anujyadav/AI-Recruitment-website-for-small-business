import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_get_jobs_feed_without_authentication():
    url = f"{BASE_URL}/api/jobs/feed"
    headers = {
        "Accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to {url} failed: {e}"

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

    try:
        jobs = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert isinstance(jobs, list), f"Response JSON is not a list but {type(jobs)}"

    for job in jobs:
        assert isinstance(job, dict), "Each job item should be a dictionary"
        # Check required fields presence (based on typical job feed fields plus walk-in badge and address if applicable)
        # We expect at least id/title/required_skills/pincode
        assert "id" in job, "Job missing 'id'"
        assert "title" in job, "Job missing 'title'"
        assert "required_skills" in job, "Job missing 'required_skills'"
        assert "pincode" in job, "Job missing 'pincode'"

        # Validate walk-in badge and address if job is walk-in
        is_walk_in = job.get("is_walk_in", False)
        if is_walk_in:
            assert "walk_in_address" in job and job["walk_in_address"], "Walk-in job missing 'walk_in_address'"
        else:
            # If not walk-in, walk_in_address may be absent or None
            pass

test_get_jobs_feed_without_authentication()