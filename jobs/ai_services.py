import json
import os
from django.conf import settings
import google.generativeai as genai

def get_model():
    api_key = getattr(settings, 'GEMINI_API_KEY', None)
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        raise ValueError("GEMINI_API_KEY is not set in settings or environment.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def assess_salary(job_title, job_skills, job_location, candidate_skills, candidate_exp, job_salary):
    """
    Uses Gemini to evaluate if the offered salary is fair for the market.
    Returns a dictionary with the assessment.
    """
    try:
        model = get_model()
    except ValueError as e:
        return {"error": str(e), "status": "Error", "message": "API key missing."}

    prompt = f"""
    You are an expert HR compensation analyst. Evaluate the following job offer:
    Job Title: {job_title}
    Required Skills: {job_skills}
    Location Pincode: {job_location}
    Offered Salary: {job_salary} INR per month
    
    Candidate Profile:
    Experience: {candidate_exp} years
    Skills: {candidate_skills}
    
    Given the current Indian job market, is this salary Fair, Below Average, or Excellent for someone with this profile?
    
    Respond STRICTLY in JSON format with the following keys:
    "status": One of "Fair", "Below Average", or "Excellent"
    "market_range": A string estimating the typical monthly salary range in INR for this role (e.g., "50,000 - 70,000 INR").
    "explanation": A brief, 2-3 sentence explanation of your verdict.
    """
    
    try:
        response = model.generate_content(prompt)
        
        # Clean up the response to ensure it's valid JSON (sometimes models wrap it in markdown block)
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
    except Exception as e:
        return {"error": str(e), "status": "Error", "message": "Failed to generate assessment."}


def generate_learning_path(job_title, job_skills, candidate_skills):
    """
    Uses Gemini to identify skill gaps and suggest a learning path.
    """
    try:
        model = get_model()
    except ValueError as e:
        return {"error": str(e), "topics": [], "message": "API key missing."}

    prompt = f"""
    You are an expert career coach and technical mentor. 
    A candidate wants to apply for the role of "{job_title}".
    
    The job requires the following skills: {job_skills}
    The candidate currently has these skills: {candidate_skills}
    
    Analyze the gap between the candidate's skills and the required skills. 
    Create a personalized, step-by-step learning roadmap focusing ONLY on the skills the candidate is missing or needs to improve for this specific job.
    
    Respond STRICTLY in JSON format with the following structure:
    {{
        "gap_analysis": "A brief 2 sentence summary of what the candidate is missing.",
        "roadmap": [
            {{
                "topic": "Name of the missing skill or concept",
                "focus_area": "What specific part to focus on",
                "estimated_time": "e.g., 2 weeks",
                "resource_suggestion": "e.g., Official Docs, specific YouTube channel type, or free online course platform"
            }}
        ]
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
    except Exception as e:
        return {"error": str(e), "topics": [], "message": "Failed to generate learning path."}
