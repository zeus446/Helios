import json
import fitz  # PyMuPDF
from openai import AsyncOpenAI
from pydantic import ValidationError
from typing import Optional, Tuple
import asyncio

from app.config import settings  
from schemas.resume import structure_resume

client = AsyncOpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.BASE_URL
)

def _sync_pdf_extractor(file_path: str) -> str:
    """Extracts layout text without locking up the async main event loop thread."""
    try:
        doc = fitz.open(file_path)
        text_blocks = []
        for page in doc:
            blocks = page.get_text("blocks")
            # Sort top-to-bottom, then left-to-right to preserve column structure accurately
            blocks.sort(key=lambda b: (b[1], b[0]))
            for b in blocks:
                if b[6] == 0:  # Text block element
                    clean_text = b[4].strip()
                    if clean_text:
                        text_blocks.append(clean_text)
        doc.close()
        return "\n".join(text_blocks)
    except Exception as e:
        print(f"[EXTRACTOR ERROR] Failed to read PDF pages: {e}")
        return ""

async def extract_text_from_pdf(file_path: str) -> str:
    return await asyncio.to_thread(_sync_pdf_extractor, file_path)

async def structureresume(raw_text: str) -> structure_resume:
    """Diagnostic version: blows up explicitly so you can see the error in the response."""
    schema_blueprint = json.dumps(structure_resume.model_json_schema(), indent=2)

    system_prompt = (
        "You are an expert resume parsing engine. Your absolute mandate is to extract EVERY piece "
        "of information from the raw resume text and map it seamlessly into the target JSON blueprint. "
        "You are strictly forbidden from omitting, truncating, or skipping any sections.\n\n"
        f"TARGET STRUCTURE BLUEPRINT:\n{schema_blueprint}\n\n"
        "CRITICAL EXTRACTION & MAPPING DIRECTIVES:\n"
        "1. EXTRACT ALL CONTACT INFO & LINKS: Look at the headers and text blocks for all digital footprint markers. "
        "Extract the email (e.g., sidds.sridhar@gmail.com), phone numbers (+917305934439), and any available LinkedIn, "
        "GitHub, or portfolio link strings. Place them accurately into their dedicated schema fields (`email`, `phoneno`, `Linked_in`, `portfolio`).\n"
        "2. MAP PATENTS TO PUBLICATIONS: Do not drop the 'PATENTS' section. You must parse the 'WEARABLE CARBON-GRAPHENE NEURAL SENSING PATCH WITH AI-DRIVEN SEIZURE PREDICTION AND IOT ALERTING FRAMEWORK' entry into the 'Publications' list array. "
        "Set 'publication_type' to 'Patent', the title to 'name', and place the full operational and signal analysis description into the 'contribution' string array.\n"
        "3. CONVERT METRICS & MILESTONES TO ACHIEVEMENTS: Do not bury key accomplishments inside experience arrays. "
        "Scan the document for major quantitative wins and organizational highlights—such as raising 21 thousand rupees for cataract surgeries "
        "during the Fueladream apprenticeship, driving massive registration traction for IEEE TEMS SRM events, or receiving the Pitch Perfect 2.0 Organizer Certificate. "
        "Map these out cleanly into the 'Acheivements' array.\n"
        "4. DEFENSIVE STRUCTURING FOR MISSING FIELDS: If optional schema fields like a specific certification 'proof', a project 'link', "
        "or text dates are completely absent or not written out as explicit strings in the raw text, set them cleanly to null or an empty string rather than throwing an exception.\n"
        "5. EXACT SCHEMA KEY ALIGNMENT: You must respect the rigid nomenclature of the blueprint schema. Ensure school layouts map directly "
        "to the 'shcool' key and experience responsibilities match the 'responsiblities' string list key exactly.\n\n"
        "OUTPUT CONSTRAINT:\n"
        "Return ONLY the raw, valid JSON object. Do not include markdown wraps or block ticks like ```json."
    )

    # 1. Test OpenRouter Call
    response = await client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free", 
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        extra_headers={
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "FastAPI Resume Parsing Engine"
        }
    )
    
    raw_output = response.choices[0].message.content
    if not raw_output:
        raise ValueError("OpenRouter returned a completely empty response string.")
        
    raw_output = raw_output.strip()
    
    if raw_output.startswith("```"):
        lines = raw_output.splitlines()
        if lines[0].startswith("```"): lines = lines[1:]
        if lines and lines[-1].startswith("```"): lines = lines[:-1]
        raw_output = "\n".join(lines).strip()

    # 2. Test JSON Parsing
    parsed_dict = json.loads(raw_output)
    
    for list_field in ["education", "experiences", "projects", "Publications", "Acheivements", "certificates"]:
        if list_field not in parsed_dict or parsed_dict[list_field] is None:
            parsed_dict[list_field] = []
            
    if "personal_info" not in parsed_dict:
        parsed_dict["personal_info"] = {"name": "Unknown Candidate"}

    # 3. Test Pydantic Validation Contract
    return structure_resume(**parsed_dict)

async def parse_resume_pipeline(file_path: str) -> Optional[Tuple[str, structure_resume]]:
    raw_text = await extract_text_from_pdf(file_path)
    if not raw_text.strip():
        print("[PIPELINE ERROR] Extracted string buffer came up empty.")
        return None
        
    structured_data = await structureresume(raw_text)  
    if not structured_data:
        print("[PIPELINE ERROR] Failed to clean up text into nested schema format.")
        return None
        
    return raw_text, structured_data