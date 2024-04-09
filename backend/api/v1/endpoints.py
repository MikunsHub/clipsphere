from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from sqlalchemy.orm import Session

from api.v1.constants import ACCESS_TOKEN_EXPIRE_MINUTES, CONFLICT_STATUS_CODE, EMAIL, USERNAME, ID
from api.v1.helpers import authenticate_user, create_access_token, decode_token, hash_password
from api.v1.schemas import ChannelData, SubscribePayload, SuccessPayload, Token, UserBase, UserCreate, UserData
from database.db_setup import get_db
from database.queries import add_subscription, create_channel, create_user, get_channel, get_subscription, get_user, remove_subscription

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.get('/')
async def index(token: str = Depends(oauth2_scheme)):
	return {'message': 'Works fine'}


@router.post('/api/auth/signup', response_model=UserBase)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
	"""add new user"""
	user = get_user(db, user_data.username)
	if user:
		raise HTTPException(status_code=CONFLICT_STATUS_CODE, detail='User already registered.')
	hashed_password = hash_password(user_data.password)
	user_data.password = hashed_password
	signedup_user = create_user(db, user_data)
	create_channel(
		db,
		ChannelData(
			channel_name=f'{signedup_user.firstname} {signedup_user.lastname}',
			description='',
			channel_owner=signedup_user.id,
		),
	)
	return signedup_user


@router.post('/api/auth/token', response_model=Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = authenticate_user(db, form_data.username, form_data.password)

	if not user:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'invalid credentials'})
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={EMAIL: user.email, USERNAME: user.username, ID: user.id}, expires_delta=access_token_expires
	)
	return Token(access_token=access_token)


async def get_current_user(token: str = Depends(oauth2_scheme)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
	)
	try:
		decoded_token = decode_token(token)
		return UserData(**decoded_token)
	except (PyJWTError, KeyError) as e:
		raise credentials_exception from e


@router.post('/api/subscription/subscribe', response_model=SuccessPayload)
def user_subscribes_to_channel(
	request_data: SubscribePayload, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)
):
	channel = get_channel(db, request_data.channel_id)
	if not channel:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'Channel not found'})
	subcription = get_subscription(db, current_user.id, channel.id)
	if subcription:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'Already subscribed to this channel'}
		)
	add_subscription(db, current_user.id, channel.id)
	return SuccessPayload(message='User successfully subscribed')


@router.post('/api/subscription/unsubscribe', response_model=SuccessPayload)
def user_unsubscribes_to_channel(
	request_data: SubscribePayload, db: Session = Depends(get_db), current_user: UserData = Depends(get_current_user)
):
	channel = get_channel(db, request_data.channel_id)
	if not channel:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'Channel not found'})
	subcription = get_subscription(db, current_user.id, channel.id)
	if not subcription:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN, detail={'error': 'User not subscribed to this channel'}
		)
	remove_subscription(db, current_user.id, channel.id)
	return SuccessPayload(message='User successfully unsubscribed')
