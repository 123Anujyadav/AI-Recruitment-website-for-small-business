# Pincode-Based Candidate Ranking

## Overview

When candidates apply for a job, their **match score** determines their rank in the employer's view.  
The system ensures that **same-pincode candidates always rank above out-of-pincode candidates**.

---

## Scoring Formula

| Component      | Points  |
|---------------|---------|
| Skill match    | 0–70 pts |
| Same pincode   | +30 pts  |
| **Maximum**    | **100 pts** |

```
skill_score  = (matched_skills / total_required_skills) × 70
location_score = 30  if candidate.pincode == job.pincode  else  0
total_score  = skill_score + location_score
```

---

## Ranking Behaviour

### Case 1 — Out-of-pincode applies, NO same-pincode applicant yet
- Score is based purely on skills (**0–70 pts**).
- Ranks normally among other out-of-pincode candidates.

### Case 2 — Out-of-pincode applies, same-pincode candidate(s) ALREADY exist
- Score is **capped just below** the lowest same-pincode applicant's score.
- Always ranks below every same-pincode candidate.

### Case 3 — Same-pincode candidate applies
- Score computed normally (skill + 30 pts).
- All **existing out-of-pincode applicants** whose score was ≥ this candidate's score are **automatically re-capped** below it.

---

## Implementation

**File:** `jobs/views.py` → `ApplyJobView.post`

```
Step 1 → Compute skill_score (0–70)
Step 2 → Check if same-pincode → add 30 pts
Step 3 → If out-of-pincode AND same-pincode applicants exist
              → cap score below lowest same-pincode score
Step 4 → Save application with final score
Step 5 → If same-pincode → re-cap existing out-of-pincode applicants
```

---

## Example

Job pincode: **400001**

| Candidate | Pincode | Skill Score | Location Bonus | Raw Score | Final Score |
|-----------|---------|-------------|----------------|-----------|-------------|
| Alice     | 400001  | 56          | +30            | 86        | **86.00**   |
| Bob       | 400001  | 42          | +30            | 72        | **72.00**   |
| Charlie   | 560001  | 70          | 0              | 70        | **71.99** *(capped below Bob)* |
| Dave      | 560001  | 35          | 0              | 35        | **35.00** *(already below)* |

> Charlie would have ranked above Bob on skill alone (70 > 72? No — but if Charlie had 73 skill score → raw 73, capped to 71.99 below Bob's 72).

---

*Last updated: 2026-03-15*
