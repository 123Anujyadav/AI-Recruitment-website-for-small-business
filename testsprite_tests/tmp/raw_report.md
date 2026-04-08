
# TestSprite AI Testing Report(MCP)

---

## 1️⃣ Document Metadata
- **Project Name:** TalentAI_MVP
- **Date:** 2026-04-02
- **Prepared by:** TestSprite AI Team

---

## 2️⃣ Requirement Validation Summary

#### Test TC001 post register with valid data
- **Test Code:** [TC001_post_register_with_valid_data.py](./TC001_post_register_with_valid_data.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/39b924eb-0fc2-41b5-9af3-0e5e1c05da1f
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC002 post login with valid credentials
- **Test Code:** [TC002_post_login_with_valid_credentials.py](./TC002_post_login_with_valid_credentials.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 43, in <module>
  File "<string>", line 30, in test_post_login_with_valid_credentials
AssertionError: Login failed: {"error":"Invalid credentials"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/8cf0a00b-e9e7-4c79-8626-67fe04cf1e04
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC003 post logout with valid session
- **Test Code:** [TC003_post_logout_with_valid_session.py](./TC003_post_logout_with_valid_session.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 56, in <module>
  File "<string>", line 36, in test_post_logout_with_valid_session
AssertionError: Login failed: {"error":"Invalid credentials"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/ee3bb86d-e8fc-4d60-914f-af9fb26e8151
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC004 get whoami with valid session
- **Test Code:** [TC004_get_whoami_with_valid_session.py](./TC004_get_whoami_with_valid_session.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 52, in <module>
  File "<string>", line 33, in test_get_whoami_with_valid_session
AssertionError: Expected 200 OK for login, got 401

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/ba09c8cd-aca1-4104-b776-3d496fb09dff
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC005 post employer job with valid data
- **Test Code:** [TC005_post_employer_job_with_valid_data.py](./TC005_post_employer_job_with_valid_data.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 52, in <module>
  File "<string>", line 29, in test_post_employer_job_with_valid_data
AssertionError: Login failed: {"error":"Invalid credentials"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/4473517d-1ef7-43c5-a913-376d7c18c7a0
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC006 get jobs feed without authentication
- **Test Code:** [TC006_get_jobs_feed_without_authentication.py](./TC006_get_jobs_feed_without_authentication.py)
- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/f9276348-32b9-4f82-8d47-b55497f06231
- **Status:** ✅ Passed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC007 put employer job edit with owner session
- **Test Code:** [TC007_put_employer_job_edit_with_owner_session.py](./TC007_put_employer_job_edit_with_owner_session.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 76, in <module>
  File "<string>", line 45, in test_put_employer_job_edit_with_owner_session
AssertionError: Login failed: {"error":"Invalid credentials"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/aea885e2-8a41-4cf3-a73c-3942227a40c9
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC008 get candidate matched jobs with valid session
- **Test Code:** [TC008_get_candidate_matched_jobs_with_valid_session.py](./TC008_get_candidate_matched_jobs_with_valid_session.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 58, in <module>
  File "<string>", line 39, in test_get_candidate_matched_jobs_with_valid_session
AssertionError: Login failed: {"error":"Invalid credentials"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/35534d4c-5936-4e0e-b085-b90df8161ea6
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC009 post candidate apply with valid data
- **Test Code:** [TC009_post_candidate_apply_with_valid_data.py](./TC009_post_candidate_apply_with_valid_data.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 88, in <module>
  File "<string>", line 28, in test_post_candidate_apply_with_valid_data
AssertionError: Expected 200 OK on login, got 401

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/aa977afb-cacc-4a9d-a445-fa957998b1f5
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---

#### Test TC010 get candidate job salary check with valid session
- **Test Code:** [TC010_get_candidate_job_salary_check_with_valid_session.py](./TC010_get_candidate_job_salary_check_with_valid_session.py)
- **Test Error:** Traceback (most recent call last):
  File "/var/task/handler.py", line 258, in run_with_retry
    exec(code, exec_env)
  File "<string>", line 61, in <module>
  File "<string>", line 29, in test_get_candidate_job_salary_check_with_valid_session
AssertionError: Login failed: 401 {"error":"Invalid credentials"}

- **Test Visualization and Result:** https://www.testsprite.com/dashboard/mcp/tests/f0c6a2f1-7e16-4d2d-a4bc-bd4c271ed8b5/acfe06ba-dbac-4eab-beb7-1e1447321eec
- **Status:** ❌ Failed
- **Analysis / Findings:** {{TODO:AI_ANALYSIS}}.
---


## 3️⃣ Coverage & Matching Metrics

- **20.00** of tests passed

| Requirement        | Total Tests | ✅ Passed | ❌ Failed  |
|--------------------|-------------|-----------|------------|
| ...                | ...         | ...       | ...        |
---


## 4️⃣ Key Gaps / Risks
{AI_GNERATED_KET_GAPS_AND_RISKS}
---