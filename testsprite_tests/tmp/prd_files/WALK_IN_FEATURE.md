# 🚶 Walk-In Job Feature

## What is Walk-In?

A **Walk-In job** is a special type of job posting where the employer invites candidates to visit a **physical address directly** — without waiting for an online shortlisting process. Instead of just applying online, candidates can show up in person.

---

## How It Works — Step by Step

### 1. Employer Posts a Walk-In Job

When an employer creates or edits a job posting, they see a checkbox:

```
☑  🚶 This is a Walk-In job
```

- If **checked** → a **Walk-In Address** text field appears.
- The employer fills in the physical venue address (e.g., `123, MG Road, Bangalore - 560001`).
- Both `is_walk_in = true` and the `walk_in_address` are saved to the database.

**Where this happens:**
- **Post New Job** form → `Employer Dashboard`
- **Edit Job** modal → allows updating the walk-in flag and address at any time

---

### 2. Walk-In Jobs Appear Differently on the Feed

All users (candidates & employers) see the **Job Feed**. Walk-In jobs display a special visual badge:

```
🚶 Walk-In
```

And if a walk-in address is provided, a green address box is shown below the job card:

```
📍 Walk-In Address: 123, MG Road, Bangalore - 560001
```

This appears in **3 places**:
| Location | Who Sees It |
|----------|-------------|
| Public Job Feed | Everyone (logged in or not) |
| Candidate Dashboard → Matched Jobs | Candidates only |
| Employer Dashboard → My Posted Jobs | Employers only |

---

### 3. Candidate Can Still Apply Online

Even if a job is Walk-In, candidates can **also** apply online using the `Apply Now` button. The system calculates a match score normally (skills + pincode). Walk-In status does **not** affect the match score — it is purely informational.

---

## Database Model

**File:** `jobs/models.py` → `Job` model

```python
is_walk_in = models.BooleanField(
    default=False,
    help_text="Whether this job accepts direct walk-ins"
)
walk_in_address = models.TextField(
    blank=True,
    default='',
    help_text="Physical address for walk-in candidates"
)
```

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `is_walk_in` | BooleanField | `False` | Marks job as walk-in |
| `walk_in_address` | TextField | `""` | Physical venue address |

---

## API Behaviour

Both fields are included in **all Job API responses** via `JobSerializer` (`fields = '__all__'`).

| Endpoint | Method | Walk-In Fields |
|----------|--------|----------------|
| `POST /api/employer/job` | POST | Accepted on creation |
| `PATCH /api/employer/job/<id>/edit` | PATCH | Can be updated anytime |
| `GET /api/jobs/feed` | GET | Returned to all viewers |
| `GET /api/candidate/matched-jobs` | GET | Returned to candidates |
| `GET /api/employer/jobs` | GET | Returned to employers |

---

## UI Behaviour Summary

```
Employer checks ☑ Walk-In
    └── Walk-In Address field appears
    └── Employer fills in address
    └── Job saved with is_walk_in=true

Job appears on Feed
    └──  🚶 Walk-In  badge shown on job card
    └── 📍 Walk-In Address box shown (if address provided)

Candidates see job on:
    └── Home Feed → can apply online AND visit in person
    └── Dashboard → Matched Jobs → same badge + address shown

Employer sees on:
    └── My Posted Jobs → same badge + address shown for reference
```

---

## Summary

| Feature | Detail |
|---------|--------|
| Who sets it | Employer (when posting or editing a job) |
| Where shown | Feed, Candidate Dashboard, Employer Dashboard |
| Affects ranking | ❌ No — purely informational |
| Online apply still works | ✅ Yes |
| Can be edited later | ✅ Yes via Edit Job modal |

---

*Last updated: 2026-03-15*
