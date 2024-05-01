from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from api.v1.constants import EXP
from api.v1.schemas import VideoUploadPayload
from env import ALGORITHM, SECRET_KEY
from shared.database.queries import get_user
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
	return pwd_context.hash(password)


def decode_token(token):
	decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
	return decoded_token


def authenticate_user(db, username: str, password: str):
	user = get_user(db, username)
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


def generate_object_key(upload_payload: VideoUploadPayload) -> str:
	# Generate a unique identifier for the object key
	unique_id = uuid.uuid4().hex

	# Get the current timestamp
	current_time = datetime.now(timezone.utc)

	timestamp = current_time.strftime('%Y%m%d%H%M%S')

	# Combine channel ID, title, timestamp, and unique ID to create the object key
	object_key = f'{upload_payload.channel_id}/{timestamp}_{upload_payload.title}_{unique_id}'

	# Replace spaces with underscores and make it lowercase
	object_key = object_key.replace(' ', '_').lower()

	return object_key
