from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import utils
from app.schemas import user
from app.database import get_db
from app.models.user import User
from app.oauth2 import create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

@router.post("/login")
async def user_login(user_credentials: user.userlogin, db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    
    result = await db.execute(select(User).filter(User.email == user_credentials.email))
    creds = result.scalar_one_or_none()

    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="invalid credentials"
        )
    
    if not utils.verify(user_credentials.password, creds.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )
    
    access_token = create_access_token(data={"user_id": creds.id})

    return {"access_token": access_token, "token_type": "bearer"}



