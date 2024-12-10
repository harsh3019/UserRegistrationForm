from fastapi import FastAPI
from config.db import Base
from sqlalchemy import Column,String,Integer,Date
from pydantic import field_validator
from sqlalchemy.sql import func






class Users(Base):
    __tablename__ = 'user_details'

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    name = Column(String(255),index=True)
    age = Column(Integer,index=True)
    address =Column(String(255),index=True)
    school_name =Column(String(255),index=True)
    unique_id = Column(Integer,unique=True,index=True)
    profile_pic = Column(String(255),index=True,nullable=True)
    created_at = Column(Date,default=func.current_date())
    
