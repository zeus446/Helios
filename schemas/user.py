from datetime import datetime

from pydantic import BaseModel, EmailStr

class usercreate(BaseModel):
    email: EmailStr
    fullname: str
    password: str

class userResponse(BaseModel):
    id: int
    fullname: str
    created_at: datetime

    class Config:
        from_attributes = True

class userlogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int