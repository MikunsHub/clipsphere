from fastapi import FastAPI
from database import models
from database.db_setup import SessionLocal, engine
from api.v1.endpoints import router as v1_router

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(v1_router, prefix='/v1')
