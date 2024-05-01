from typing import Any, Generator
from sqlalchemy.orm.session import Session
from shared.database.constants import DATABASE_DRIVER
from env import PG_USER, PG_PASSWORD, PG_HOST, PG_NAME, PG_PORT
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = URL.create(
	drivername=DATABASE_DRIVER,
	username=PG_USER,
	password=PG_PASSWORD,
	host=PG_HOST,
	database=PG_NAME,
	port=PG_PORT,  # type: ignore
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, Any, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
