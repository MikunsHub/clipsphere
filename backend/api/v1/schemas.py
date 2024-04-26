from typing import Optional, Union
from pydantic import BaseModel
from pydantic import EmailStr

from database.models import VideoFormat


class UserBase(BaseModel):
	email: EmailStr


class UserCreate(UserBase):
	email: EmailStr
	username: str
	lastname: str
	firstname: str
	password: str
	confirm_password: str


class UserData(BaseModel):
	id: int
	email: EmailStr
	username: str


class Token(BaseModel):
	access_token: str


class TokenData(BaseModel):
	username: Union[str, None] = None


class ChannelData(BaseModel):
	channel_name: str
	description: str
	channel_owner: int


class SubscribePayload(BaseModel):
	channel_id: int


class SuccessPayload(BaseModel):
	message: str
	data: Optional[dict] = None


class VideoUploadPayload(BaseModel):
	channel_id: int
	title: str
	description: str
	video_format: VideoFormat

	@classmethod
	def __get_validators__(cls):
		yield cls.validate_video_format

	@classmethod
	def validate_video_format(cls, v):
		if isinstance(v, VideoFormat):
			return v
		if isinstance(v, str) and v.lower() in [format.value for format in VideoFormat]:
			return VideoFormat(v.lower())
		raise ValueError(f'Invalid video format. Allowed values: {", ".join(format.value for format in VideoFormat)}')


class VideoMetadata(BaseModel):
	channel_id: int
	title: str
	description: str
	video_format: VideoFormat
	raw_url: str
	view_count: Optional[int] = 0
	like_count: Optional[int] = 0
