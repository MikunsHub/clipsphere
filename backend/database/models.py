from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
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


class Users(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	password = Column(String)
	is_active = Column(Boolean, default=False)
	is_superuser = Column(Boolean, default=False)
	firstname = Column(String, index=True)
	lastname = Column(String, index=True)
	channel_name = Column(String, index=True)

	videos = relationship('Video', back_populates='user')


class Video(Base):
	__tablename__ = 'videos'

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	description = Column(String)
	upload_date = Column(DateTime)
	view_count = Column(Integer, default=0)
	like_count = Column(Integer, default=0)
	quality = Column(ENUM(*[x.value for x in VideoQuality], name='video_quality_type'), default=VideoQuality.p360.value)  # type: ignore
	raw_url = Column(String, index=True)
	processed_url = Column(String, index=True)
	user_id = Column(Integer, ForeignKey('users.id'))

	user = relationship('User', back_populates='videos')
