import os
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
# from .config import settings

from . import schemas, database, models
from .database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
access_token_expire_minutes = 30
algorithm = "HS256"
secret_key="sadkjkasdfjalksdfjlisadjliasjfliasjhfiasfjksalfhjjsafgadhjfg"


def create_access_token(data: dict):
    to_encode = data.copy()
    # Use the expiration time from settings
    expire = datetime.now() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({"exp": expire})
    # Use the secret key and algorithm from settings
    encode_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encode_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        # Use the secret key and algorithm from settings
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
