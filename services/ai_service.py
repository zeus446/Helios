import json
import logging
from typing import Union
from openai import AsyncOpenAI  # Use the async client
from app.config import settings
from models.resume import Master_resume_DB


# Set up basic logging
logger = logging.getLogger(__name__)

# Initialize the ASYNC client globally
client = AsyncOpenAI(
    base_url=settings.BASE_URL,
    api_key=settings.OPENROUTER_API_KEY
)

def clean_json_response(text: str) -> dict:
    """Cleans markdown formatting and parses JSON safely."""
    # Strip markdown backticks more defensively
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
        
    if text.endswith("```"):
        text = text[:-3]
        
    text = text.strip()
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}. Raw text: {text}")
        return {} # Return empty dict or raise a custom API exception

async def parse_resume_to_structured(raw_input: str) -> dict:
    prompt = (
        "You are an expert HR data extraction system. Parse the following resume into structured JSON.\n"
        "Return ONLY valid JSON. Do not include any text outside the JSON object.\n\n"
        "Strict JSON Schema:\n"
        "{\n"
        "  \"personal_info\": {\"name\": \"\", \"email\": \"\", \"phone\": \"\"},\n"
        "  \"experiences\": [{\"company\": \"\", \"title\": \"\", \"dates\": \"\", \"responsibilities\": [\"\"]}],\n"
        "  \"projects\": [{\"name\": \"\", \"description\": \"\", \"tech_stack\": [\"\"]}],\n"
        "  \"skills\": [\"\"],\n"
        "  \"education\": [{\"school\": \"\", \"degree\": \"\", \"year\": \"\"}],\n"
        "  \"certifications\": [\"\"],\n"
        "  \"achievements\": [\"\"]\n"
        "}\n\n"
        "Resume to parse:\n"
        f"{raw_input}"
    )

    try:
        response = await client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        
        content = response.choices[0].message.content
        parsed = clean_json_response(content)
        if not isinstance(parsed, dict):
            logger.error("Parsed response is not a dict")
            return {}

        return {
            "personal_info": parsed.get("personal_info", {}),
            "experiences": parsed.get("experiences", []),
            "projects": parsed.get("projects", []),
            "skills": parsed.get("skills", []),
            "education": parsed.get("education", []),
            "certifications": parsed.get("certifications", []),
            "achievements": parsed.get("achievements", []),
        }

    except Exception as e:
        logger.error(f"LLM API Call failed: {e}")
        return {}

async def analyze_job_description(job_description: str) -> str:
    prompt = f"""
    You are an expert technical recruiter and Applicant Tracking System (ATS) analyst. 
    Your task is to analyze the provided job description and extract key requirements into a strict JSON format.

    Return ONLY valid JSON. Do not include any introductory or concluding text.
    
    The JSON must contain EXACTLY these top-level keys with the specified data types:
    - "required_skills": list of strings (hard skills explicitly stated as required)
    - "preferred_skills": list of strings (skills listed as nice-to-have or preferred)
    - "ats_keywords": list of strings (critical industry jargon, tools, and methodologies for ATS optimization)
    - "core_competencies": list of strings (soft skills and behavioral traits)
    - "company_values": list of strings (inferred or explicitly stated cultural values)
    - "top_3_priorities": list of strings (the 3 most critical responsibilities or goals of the role)
    - "experience_level": string (e.g., "Entry-level", "Mid-level", "Senior", "Executive")
    - "role_focus": string (a concise 1-sentence summary of the main objective of this position)

    If a specific category cannot be found or inferred from the text, return an empty list or null for that key.

    Job Description:
    {job_description}
    """

    try:
        response = await client.chat.completions.create(
            model="openrouter/free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0   
        )

        content = response.choices[0].message.content
        parsed = clean_json_response(content)
        if not isinstance(parsed, dict):
            logger.error("Parsed response is not a dict")
            return {}

        return parsed

    except Exception as e:
        logger.error(f"LLM API Call failed: {e}")
        return {}

async def tailor_resume(master_resume: dict, job_analysis: dict, job_description: str) -> dict:
    master_resume_str = json.dumps(master_resume)
    job_analysis_str = json.dumps(job_analysis)
    prompt = f"""
    You are an expert career coach and professional resume writer. 
    Your task is to tailor the provided resume to better align with the target job description.

    CRITICAL RULE: Do NOT invent or hallucinate any new job titles, companies, certifications, or experiences. You may only rephrase, reword, and reorder the existing information to highlight relevant skills and match the job's keywords.

    Return ONLY valid JSON. Do not include any introductory or concluding text, and do not wrap the JSON in markdown code blocks.
    
    The JSON structure must contain EXACTLY these top-level keys:
    - "tailored_summary": string (a compelling 3-4 sentence professional summary positioned for this specific role)
    - "experiences": list of dicts (must keep the original company, title, and dates, but rewrite the bullet points/responsibilities to use ATS keywords)
    - "projects": list of dicts (must keep original names, but rewrite descriptions to highlight relevant technologies)
    - "optimized_skills": list of strings (a curated list of the user's existing skills, maximum 15 items, ordered by relevance)
    - "certifications": list of strings (the user's existing certifications, reordered by relevance)
    - "achievements": list of strings (the user's existing achievements, rephrased to highlight matching metrics)
    - "tailoring_strategies": list of strings (a summary explaining the strategic changes made)

    STRATEGY RULES:
    1. DROP any experience from the "experiences" list that has zero relevant responsibilities rather than keeping it empty.
    2. REMOVE skills from "optimized_skills" that are clearly irrelevant to the target role.
    3. If an experience bullet point cannot be meaningfully connected to the job description, rewrite it to emphasize transferable skills or drop it entirely.

    Original Resume:
    {master_resume_str}
    
    Target Job Description:
    {job_analysis_str}
    """
    try:
        print("MASTER STRUCTURED DATA:", Master_resume_DB.structured_data)
        response = await client.chat.completions.create(
               model="openrouter/free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0   
        )
        content = response.choices[0].message.content
        print("TAILOR RAW RESPONSE:", content[:1000])

        content = response.choices[0].message.content
        parsed = clean_json_response(content)
        if not isinstance(parsed, dict):
            logger.error("Parsed response is not a dict")
            return {}
        
        return {
    "tailored_summary": parsed.get("tailored_summary", ""),
    "experiences": parsed.get("experiences", []),
    "projects": parsed.get("projects", []),
    "optimized_skills": parsed.get("optimized_skills", []),
    "certifications": parsed.get("certifications", []),
    "achievements": parsed.get("achievements", []),
    "tailoring_strategies": parsed.get("tailoring_strategies", []),
}
        
    except Exception as e:
        logger.error(f"LLM call failed {e}")
        return {}

    





