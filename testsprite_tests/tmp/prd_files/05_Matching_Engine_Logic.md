# Matching Engine Logic

## Step 1: Skill Matching

matched_skills = common skills count total_required = job required
skills count skill_score = (matched_skills / total_required) \* 70

## Step 2: Location Matching

If candidate_pincode == job_pincode: location_score = 30 Else:
location_score = 0

## Final Score

total_score = skill_score + location_score

## Ranking

Sort candidates in descending order by total_score
