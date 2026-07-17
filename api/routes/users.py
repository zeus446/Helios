from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app import utils
from schemas.user import usercreate
from app.database import get_db
from models.user import User
from app.oauth2 import get_current_user
from schemas.user import TokenData
from sqlalchemy import select


router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post('/create', status_code=status.HTTP_201_CREATED)
async def user_create(user_data: usercreate, db: AsyncSession = Depends(get_db)):
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


@router.delete('/me',status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db:AsyncSession=Depends(get_db),current_user :TokenData=Depends(get_current_user)):
    query = select(User).where(User.id == current_user.id)

    user = await db.execute(query)

    current = user.scalar_one_or_none()

    if current is None:
        raise   HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no such user"
        )
    
    await db.delete(current)
    await db.commit()

    return {"message":"sucessfully deleted account"}




