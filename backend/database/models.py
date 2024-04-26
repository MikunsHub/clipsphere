from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from database.db_setup import Base


class VideoQuality(Enum):
	p240 = '240p'
	p360 = '360p'
	p480 = '480p'
	p720 = '720p'
	p1080 = '1080p'
	p4K = '4K'


class VideoFormat(Enum):
	MP4 = 'mp4'
	AVI = 'avi'
	MOV = 'mov'
	MKV = 'mkv'
	WEBM = 'webm'


class Users(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	username = Column(String, unique=True, index=True)
	password = Column(String)
	is_active = Column(Boolean, default=False)
	is_superuser = Column(Boolean, default=False)
	firstname = Column(String, index=True)
	lastname = Column(String, index=True)

	subscriptions = relationship('Channels', secondary='subscriptions')


class Channels(Base):
	__tablename__ = 'channels'

	id = Column(Integer, primary_key=True, index=True)
	channel_name = Column(String, index=True)
	channel_description = Column(String, index=True)
	channel_owner = Column(Integer, ForeignKey('users.id'))

	subscribers = relationship('Users', secondary='subscriptions')
	videos = relationship('Video', back_populates='channel')


class Subscription(Base):
	__tablename__ = 'subscriptions'

	user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
	channel_id = Column(Integer, ForeignKey('channels.id'), primary_key=True)


class Video(Base):
	__tablename__ = 'videos'

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String)
	upload_date = Column(DateTime, server_default=text('now()'))
	updated_at = Column(DateTime, server_default=text('now()'))
	view_count = Column(Integer, default=0)
	like_count = Column(Integer, default=0)
	quality = Column(ENUM(*[x.value for x in VideoQuality], name='video_quality_type'))  # type: ignore
	video_format = Column(ENUM(*[x.value for x in VideoFormat], name='video_format_type'))  # type: ignore
	raw_url = Column(String, index=True)
	processed_url = Column(String, index=True)
	channel_id = Column(Integer, ForeignKey('channels.id'))

	channel = relationship('Channels', back_populates='videos')
