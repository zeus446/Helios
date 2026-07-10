from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import utils
from app.schemas import user
from app.database import get_db
from app.models.user import User
from app.oauth2 import create_access_token, get_current_user

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def user_create(user_data: user.usercreate, db: AsyncSession = Depends(get_db)):
    hashed_password = utils.hash(user_data.password)
    
    # Extract fullname, email, and password as a dict
    user_dict = user_data.dict()
    
    # Remove the plain text 'password' so the DB doesn't reject it
    user_dict.pop('password', None)
    
    # Inject the hashed password under the column name your DB expects
    user_dict['hashed_password'] = hashed_password
    
    # This now unpacks: fullname, email, and hashed_password
    new_user = User(**user_dict)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user