from datetime import datetime, timedelta
from typing import Union
import jwt
from api.v1.constants import EXP
from env import ALGORITHM, SECRET_KEY
from database.queries import get_user_by_email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
	return pwd_context.hash(password)


def authenticate_user(db, email: str, password: str):
	user = get_user_by_email(db, email)
	if not user:
		return False
	if not verify_password(password, user.password):
		return False
	return user


def create_access_token(*, data: dict, expires_delta: Union[timedelta, None] = None):
	to_encode = data.copy()
	if expires_delta:
		expire = datetime.utcnow() + expires_delta
	else:
		expire = datetime.utcnow() + timedelta(minutes=15)
	to_encode.update({EXP: expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt
