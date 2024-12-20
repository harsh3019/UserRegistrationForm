from fastapi import FastAPI 
from sqlalchemy.orm import declarative_base,sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

DATABASE_URL =  os.getenv('DB_URL')
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()