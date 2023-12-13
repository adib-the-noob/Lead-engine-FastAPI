import os
import shutil
import uuid 
import urllib


from typing import Annotated
from datetime import datetime, timedelta

from fastapi import HTTPException, status, Depends, UploadFile
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from db import db_dependency
from models.user_models import User, UserRoles
from config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(
    db: Annotated[db_dependency, Depends(db_dependency)],
    full_name: str,
    password: str,
    email: str,
    phone_number: str,
    profile_picture: str,
    role: UserRoles,
) -> User:
    user = User(
        full_name=full_name,
        email=email,
        phone_number=phone_number,
        role=role,
        profile_picture=profile_picture,
        password=get_password_hash(password),
    )
    user.save(db)
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=config.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM
    )
    return encoded_jwt


def get_user(email: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def authenticate_user(db: db_dependency, email: str, password: str):
    user = get_user(email, db)
    if not verify_password(password, user.password):
        return False
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email, db)
    if user is None:
        raise credentials_exception
    return user


user_dependency = Annotated[User, Depends(get_current_user)]


def save_image(
    image: UploadFile, save_to_folder: str
):
    name = image.filename
    if not os.path.exists(save_to_folder):
        os.makedirs(save_to_folder)
    if name is None:
        name = uuid.uuid4()
    image_path = f"{save_to_folder}/{name}"
    image_url = urllib.parse.quote(image_path)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    return image_url