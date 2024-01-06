from api.v1.schemas import UserCreate
from sqlalchemy.orm import Session

from .models import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email, lastname=user.lastname, firstname=user.firstname, password=user.password, is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
