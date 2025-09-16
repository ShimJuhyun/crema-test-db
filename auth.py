from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import bcrypt
import jwt  # pyjwt

KST = ZoneInfo("Asia/Seoul")
SECRET_KEY = "vk4PMayQk9NzAu8OheILnvB8qNAS6A2RTRVoZq2K31s"
REFRESH_SECRET_KEY = "0gRlzvP5ppSoKTPKkCNcok5VDXxRakE4GmbhOxLGM_s"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # tokenUrl은 무시해도 됨

def hash_password(plain_password: str) -> str:
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def get_exp(expires_delta: timedelta):
    expire = datetime.now(tz=KST) + expires_delta
    return expire

def verify_password(plain_password: str, hashed_str: str) -> bool:
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_str.encode('utf-8')
    # print(plain_password, hashed_str)
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def create_access_jwt(data: dict, exp: datetime):
    to_encode = data.copy()
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def create_refresh_jwt(data: dict, exp):
    to_encode = data.copy()
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm="HS256")

def validate_access_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="AccessToken expired")
    
def validate_refresh_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms="HS256")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"user_id": user_id}
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="RefreshToken expired")
