from datetime import datetime
from pydantic import BaseModel, EmailStr

class Master_resume(BaseModel):
    user_id = int 
    raw_text = str
    structured_data = str
    created_at = datetime


