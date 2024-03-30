from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.v1.constants import (
	ACCESS_TOKEN_EXPIRE_MINUTES,
	CONFLICT_STATUS_CODE,
	SUB,
)
from api.v1.helpers import authenticate_user, create_access_token, hash_password
from api.v1.schemas import Token, UserBase, UserCreate
from database.db_setup import get_db
from database.queries import create_user, get_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/')
async def index(token: str = Depends(oauth2_scheme)):
	return {'message': 'Works fine'}


@router.post('/token', response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = authenticate_user(db, form_data.username, form_data.password)

	if not user:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'invalid credentials'})
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(data={SUB: user.email}, expires_delta=access_token_expires)
	return Token(access_token=access_token)


@router.post('/api/auth/signup', response_model=UserBase)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
	"""add new user"""
	user = get_user(db, user_data.username)
	if user:
		raise HTTPException(status_code=CONFLICT_STATUS_CODE, detail='User already registered.')
	hashed_password = hash_password(user_data.password)
	user_data.password = hashed_password
	signedup_user = create_user(db, user_data)
	return signedup_user
