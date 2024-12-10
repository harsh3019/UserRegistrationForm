from fastapi import FastAPI
from api.user_root import userapi
from config.db import Base,engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(userapi, prefix='/users', tags=['users'])





