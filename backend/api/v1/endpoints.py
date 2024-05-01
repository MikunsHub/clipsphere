from datetime import timedelta

from api.v1.constants import ACCESS_TOKEN_EXPIRE_MINUTES, CONFLICT_STATUS_CODE, EMAIL, ID, USERNAME
from api.v1.helpers import authenticate_user, create_access_token, decode_token, generate_object_key, hash_password
from api.v1.schemas import (
	ChannelData,
	SubscribePayload,
	SuccessPayload,
	Token,
	UserBase,
	UserCreate,
	UserData,
	VideoMetadata,
	VideoUploadPayload,
)
from shared.database.db_setup import get_db
from shared.database.queries import (
	add_subscription,
	add_video_metadata,
	create_channel,
	create_user,
	get_channel,
	get_subscription,
	get_user,
	remove_subscription,
)
from env import AWS_S3_RAW_VIDEOS_BUCKET_NAME, LOCAL, LOCALSTACK_ENDPOINT_URL, TOKEN_URL
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from sqlalchemy.orm import Session

from shared.s3_client import S3Config, S3Interface

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


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


@router.post('/api/videos/upload', response_model=SuccessPayload)
async def user_gets_presigned_url_and_saves_video_metadata(
	request_body: VideoUploadPayload,
	db: Session = Depends(get_db),
	current_user: UserData = Depends(get_current_user),
):
	channel = get_channel(db, request_body.channel_id)
	if not channel:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Channel not found')
	try:
		config = S3Config(localstack_endpoint_url=LOCALSTACK_ENDPOINT_URL, local=LOCAL)
		s3_client = S3Interface(config)
		object_key = generate_object_key(request_body)
		presigned_url = s3_client.generate_presigned_url(AWS_S3_RAW_VIDEOS_BUCKET_NAME, object_key, 86400)
		vid_metadata = VideoMetadata(**request_body.__dict__, raw_url=presigned_url)
		add_video_metadata(db, vid_metadata)
	except Exception:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to upload video')

	return SuccessPayload(message='Video uploaded successfully!', data={'url': presigned_url, 'object_key': object_key})
