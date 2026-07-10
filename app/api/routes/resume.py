from fastapi import APIRouter,UploadFile,HTTPException,status,File,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.resume import MasterResume,TailoredResume
from app.services.resume_parser import extract_text_from_pdf
from app.services.ai_service import (
    parse_resume_to_structured,
    analyze_job_description,
    tailor_resume as tailor_resume_ai  # rename it on import
)
import asyncio

router = APIRouter(
    prefix="/resume",
    tags=['Resume']
)

@router.post("/upload")
async def upload_resume(file:UploadFile = File(...),db:AsyncSession=Depends(get_db)):

    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file is not of the form of pdf"
        )

    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    stuctured = await parse_resume_to_structured(text)
    master_resume = MasterResume(
        user_id = 1,
        raw_text = text,
        structured_data = stuctured
    )

    db.add(master_resume)
    await db.commit()
    await db.refresh(master_resume)

    return master_resume


@router.post("/tailor")
async def tailor_resume_endpoint(job_desription:str,job_title:str,company_name:str,db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(MasterResume).where(MasterResume.user_id == 1))
    master = result.scalars().first()
    if master is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="no resume found"
        )
    analyse, _ = await asyncio.gather(
    analyze_job_description(job_desription),
    asyncio.sleep(0)  # placeholder
)
    tailor = await tailor_resume_ai(master.structured_data,analyse,job_desription)
    calculated_score = analyse.get("ats_score",70)

    Tailor_resume = TailoredResume(
        master_resume_id = master.id,
        user_id = 1,
        job_description = job_desription,
        job_title = job_title,
        company_name = company_name,
        tailored_content = tailor,
        tailoring_notes = analyse,
        ats_score = calculated_score
    )

    db.add(Tailor_resume)
    await db.commit()
    await db.refresh(Tailor_resume)

    return Tailor_resume




