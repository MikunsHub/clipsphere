from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
   email: EmailStr

class UserCreate(UserBase):
   email: EmailStr
   lastname: str
   firstname: str
   password: str