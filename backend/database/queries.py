from api.v1.schemas import UserCreate
from sqlalchemy.orm import Session

from .models import Users


def get_user(db: Session, username: str):
	return db.query(Users).filter(Users.username == username).first()


def create_user(db: Session, user: UserCreate):
	db_user = Users(
		email=user.email,
		username=user.username,
		lastname=user.lastname,
		firstname=user.firstname,
		password=user.password,
		is_active=True,
	)
	db.add(db_user)
	db.commit()
	db.refresh(db_user)
	return db_user
