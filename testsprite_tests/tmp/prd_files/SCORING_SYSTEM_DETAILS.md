# TalentAI Scoring System Details

This document explains how the "Match Score" is calculated for candidates when they apply for a job in the Talent Code platform.

## Overview

The scoring system evaluates candidates based on two primary factors: **Skills** and **Location (Pincode)**. It also implements a unique ranking rule that prioritizes local candidates regardless of their raw skill match.

---

## Scoring Factors

The total score is a combination of two components:

### 1. Skill Score (Max 70 points)
*   **Logic**: The system compares the candidate's skills (from their profile) with the job's required skills.
*   **Calculation**: 
    `skill_score = (matched_skills / total_required_skills) * 70`
*   **Edge Case**: If a job has no required skills specified, the candidate automatically receives a full 70 points for the skill component.

### 2. Location Score (Max 30 points)
*   **Logic**: The system checks if the candidate's pincode matches the job's pincode exactly.
*   **Calculation**:
    *   **Match**: 30 points
    *   **No Match**: 0 points

### Raw Total Score
`total_score = skill_score + location_score`

---

## The "Local Priority" Ranking Rule (Pincode-Aware)

To ensure local candidates are always prioritized for employers, the system enforces a strict relative ranking rule:

> **Rule**: If ANY candidate with a matching pincode applies for a job, they MUST rank higher than ALL candidates with non-matching pincodes.

### How it is enforced:
1.  **When a Non-Local candidate applies**:
    *   The system checks if any local candidates have already applied.
    *   If yes, the non-local candidate's score is **capped** to just below the lowest local candidate's score (`lowest_local_score - 0.01`).
2.  **When a Local candidate applies**:
    *   The system identifies all existing non-local applicants for that job.
    *   If any non-local applicant has a score higher than or equal to the new local candidate's score, their score is **downgraded** to just below the new local candidate's score (`new_local_score - 0.01`).

This ensures that the "Recommended" list (usually candidates with 75% match or higher) naturally prioritizes local talent while still accounting for their skills.

---

## Code References

The scoring logic is primarily implemented in the following files:

| File | Component | Description |
| :--- | :--- | :--- |
| [`jobs/views.py`](file:///c:/Users/adity/Downloads/Talent%20Code/TalentAI_MVP/jobs/views.py) | `ApplyJobView.post` | The core logic for calculating and capping scores (Lines 115–173). |
| [`jobs/models.py`](file:///c:/Users/adity/Downloads/Talent%20Code/TalentAI_MVP/jobs/models.py) | `Application.match_score` | Data model field where the score is stored as a `FloatField`. |
| [`jobs/serializers.py`](file:///c:/Users/adity/Downloads/Talent%20Code/TalentAI_MVP/jobs/serializers.py) | `ApplicationSerializer` | Exposes the score to the frontend (aliased as `candidate_eval_score`). |
| [`templates/index.html`](file:///c:/Users/adity/Downloads/Talent%20Code/TalentAI_MVP/templates/index.html) | Frontend Filter | Defines "Recommended" as candidates with `match_score >= 75`. |

---

*Last Updated: March 27, 2026*
