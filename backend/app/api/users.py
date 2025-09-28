from fastapi import APIRouter, HTTPException, status, Depends
from app.models.schemas import UserCreate, LoginRequest, UserSchema
from app.services.user_services import create_user, get_current_user_dep, login_user
from app.models.models import User
from app.db import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    try:
        # Create a new session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        print(f"DATABASE_CONNECTION_ERROR {e}")
        raise e

@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_info = User(username=user.username, email=user.email, password_hash=user.password)
    return create_user(user_info, db)

@router.post("/login")
async def login(user: LoginRequest, db: Session = Depends(get_db)):
    email = user.email
    password = user.password
    return login_user(email, password, db)

@router.get("/me", response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user_dep)):
    return current_user