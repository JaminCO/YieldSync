from app.models.models import User
from app.db import get_db
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
import os
import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key") 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24  # 1 day

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None

def get_current_user(token: str, db: Session):
    payload = verify_jwt_token(token)
    if payload:
        user_id = payload.get("user_id")
        if user_id:
            return db.query(User).filter(User.id == user_id).first()
    return None

def get_current_user_dep(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def create_user(user: User, db: Session):
    user.password_hash = hash_password(user.password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_jwt_token({"sub": user.email, "user_id": user.id})
    return {"user": user, "access_token": token}

def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    if user and verify_password(password, user.password_hash):
        token = create_jwt_token({"sub": user.email, "user_id": user.id})
        return {"user": user, "access_token": token}
    return None

def get_user_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()