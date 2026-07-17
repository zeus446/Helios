from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from schemas.user import userlogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from models.user import User
from app.oauth2 import create_access_token

from app.utils import verify

router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

@router.post('/login')
async def user_login(user_credentilas:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    query = select(User).where(User.email == user_credentilas.username)
    creds = await db.execute(query)
    result = creds.scalar_one_or_none()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID CREDENTIALS"
        )
    
    if not verify(user_credentilas.password,result.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )
    
    access_token = create_access_token(data = {"user_id":result.id})

    return {"access_token":access_token,"token_type":"bearer token"}
        

    