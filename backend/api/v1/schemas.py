from typing import Optional, Union
from pydantic import BaseModel
from pydantic import EmailStr


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
