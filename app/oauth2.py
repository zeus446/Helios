from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

# ⚠️ PRO-TIP: Avoid hardcoding your secret key directly in production code. 
# Keep this in an environment variable (e.g., os.environ.get("SECRET_KEY"))!
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()

    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 🔍 Look at your terminal console when you hit Execute!
        print(f"👉 YOUR ACTUALLY RECEIVED JWT PAYLOAD IS: {payload}")
        
        user_id = payload.get("id")

        if user_id is None:
            raise credentials_exception
        
        token_data = TokenData(id=user_id)
        return token_data  
        
    except JWTError:
        raise credentials_exception
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    # 🚀 Move these INSIDE the function so FastAPI doesn't turn them into UI input boxes
    detail_message = "Could not validate credentials"
    exception_headers = {"WWW-Authenticate": "Bearer"}
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail_message,
        headers=exception_headers
    )

    return verify_access_token(token, credentials_exception)