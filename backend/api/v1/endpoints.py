from api.v1.schemas import UserBase, UserCreate
from api.v1.helpers import hash_password
from database.db_setup import get_db
from database.queries import create_user, get_user_by_email
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/home")
async def root():
    return {"message": "Home is wherever I'm with you"}


@router.post("/api/auth/signup", response_model=UserBase)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """add new user"""
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(status_code=409, detail="Email already registered.")
    hashed_password = hash_password(user_data.password)
    user_data.password = hashed_password
    signedup_user = create_user(db, user_data)
    return signedup_user


@router.get("/users/{email}", response_model=UserBase)
def read_user(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
