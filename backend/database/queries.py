from datetime import datetime
from api.v1.schemas import UserCreate, ChannelData, VideoMetadata
from sqlalchemy.orm import Session

from .models import Channels, Subscription, Users, Video


def get_user(db: Session, username: str):
	return db.query(Users).filter(Users.username == username).first()


def get_channel(db: Session, channel_id: int):
	return db.query(Channels).filter(Channels.id == channel_id).first()


def get_channel_by_username(db: Session, username: str):
	channel_owner = (
		db.query(Users, Channels)
		.filter(Users.username == username)
		.join(Channels, Channels.channel_owner == Users.id)
		.first()
	)
	if channel_owner:
		return channel_owner[0]  # Return the user object
	else:
		return None


def get_subscription(db: Session, user_id: int, channel_id: int):
	return db.query(Subscription).get((user_id, channel_id))


def create_user(db: Session, user: UserCreate):
	db_user = Users(
		email=user.email,
		username=user.username,
		lastname=user.lastname,
		firstname=user.firstname,
		password=user.password,
		is_active=True,  # TODO: email verification
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user


def create_channel(db: Session, channel_data: ChannelData):
	db_channel = Channels(
		channel_name=channel_data.channel_name,
		channel_description=channel_data.description,
		channel_owner=channel_data.channel_owner,
	)
	db.add(db_channel)
	db.commit()
	db.refresh(db_channel)
	return db_channel


def add_subscription(db: Session, user_id: int, channel_id: int):
	db_subcription = Subscription(user_id=user_id, channel_id=channel_id)
	db.add(db_subcription)
	db.commit()
	db.refresh(db_subcription)
	return db_subcription


def remove_subscription(db: Session, user_id: int, channel_id: int):
	subscription = db.query(Subscription).filter_by(user_id=user_id, channel_id=channel_id).first()
	db.delete(subscription)
	db.commit()


def add_video_metadata(db: Session, metadata: VideoMetadata):
	video_metadata = Video(
		title=metadata.title,
		description=metadata.description,
		upload_date=datetime.now(),
		video_format=metadata.video_format.value,
		raw_url=metadata.raw_url,
		channel_id=metadata.channel_id,
	)
	db.add(video_metadata)
	db.commit()
	db.refresh(video_metadata)
	return video_metadata
