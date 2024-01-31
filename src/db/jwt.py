import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from typing import Annotated, Union
from pydantic import BaseModel
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
KEY=os.environ.get("KEY")
ALGORITHM=os.environ.get("ALGORITHM")


class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    
    if expires_delta:
        # Adds expiration time to the token, using either the provided timedelta 
        expire = datetime.utcnow() + expires_delta
    else:
        # or a default of 15 minutes(Standard expiration time)
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    return email

    