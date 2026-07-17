from fastapi import APIRouter,HTTPException,Depends,status,UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from schemas.resume import Master_resume_DB
import os
import secrets
from services.resume_parser import parse_resume_pipeline
from app.oauth2 import get_current_user

router = APIRouter(
    prefix='/resume',
    tags=['resume functions']
)

UPLOAD_DIR = "./uploadedresumes_pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

@router.post("/upload",status_code=status.HTTP_201_CREATED)
async def upload_resume(file:UploadFile,db:AsyncSession=Depends(get_db),user_id:int=Depends(get_current_user)):
    doc = file.filename
    if doc.endswith('.pdf') == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="file ios not a pdf"
        )
    

    random_hex = secrets.token_hex(8)
    safe_filename = f"{random_hex}.pdf"
    file_path = os.path.join(UPLOAD_DIR,safe_filename)

    try:
        with open(file_path,"wb") as local_file:
            while chunk := await file.read(1024*1024):
                local_file.write(chunk)
        parser = await parse_resume_pipeline(file_path)
        if parser is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="parsing engine could not stract structure"
            )
        
        plain_text,structured_data = parser
        structured_dict = structured_data.model_dump()

        master_resume = Master_resume_DB(
            user_id = user_id.user_id,
            raw_text=plain_text,
            structured_data=structured_dict
        )
        db.add(master_resume)
        await db.commit()
        await db.refresh(master_resume)
        return {"status":"success","id":master_resume.user_id}

        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"CRITICAL ERROR TRACEBACK: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="failed to write disk"
        )
    
    finally:
        await file.close()
        if os.path.exists(file_path):
            os.remove(file_path)
        
