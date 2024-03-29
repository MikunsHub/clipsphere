from typing import Union
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


class UserSignin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str


class TokenData(BaseModel):
	username: Union[str, None] = None
