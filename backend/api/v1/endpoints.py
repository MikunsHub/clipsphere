from datetime import timedelta
from api.v1.schemas import UserBase, UserCreate, Token, UserSignin
from api.v1.helpers import hash_password, authenticate_user, create_access_token
from api.v1.constants import (
	ACCESS_TOKEN_EXPIRE_MINUTES,
	CONFLICT_STATUS_CODE,
	NOT_FOUND_STATUS_CODE,
	SUB,
	WWW_AUTHENTICATE,
	Bearer,
)
from database.db_setup import get_db
from database.queries import create_user, get_user_by_email
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter()


@router.get('/home')
async def root():
	return {'message': "Home is wherever I'm with you"}


@router.post('/api/auth/signup', response_model=UserBase)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
	"""add new user"""
	user = get_user_by_email(db, user_data.email)
	if user:
		raise HTTPException(status_code=CONFLICT_STATUS_CODE, detail='Email already registered.')
	hashed_password = hash_password(user_data.password)
	user_data.password = hashed_password
	signedup_user = create_user(db, user_data)
	return signedup_user


@router.post('/token', response_model=Token)
async def user_login(form_data: UserSignin, db: Session = Depends(get_db)):
	user = authenticate_user(db, form_data.email, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect username or password',
			headers={WWW_AUTHENTICATE: Bearer},
		)
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(data={SUB: user.email}, expires_delta=access_token_expires)
	return Token(access_token=access_token)


@router.get('/users/{email}', response_model=UserBase)
def read_user(email: str, db: Session = Depends(get_db)):
	db_user = get_user_by_email(db, email=email)
	if db_user is None:
		raise HTTPException(status_code=NOT_FOUND_STATUS_CODE, detail='User not found')
	return db_user
