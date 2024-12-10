from fastapi import FastAPI
from  pydantic import BaseModel,field_validator
from typing import Optional
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    name : str 
    age  : int
    address : str
    school_name : str
    unique_id : int
    created_at: date = date.today()
    profile_pic: Optional[str] = None


    @field_validator("age")
    def validate_age(cls, value):
        if value <= 18:
            raise ValueError("Age must be greater than 18")
        return value

class UserResponse(BaseModel):

        id :int
        name : str 
        age  : int
        address : str
        school_name : str
        unique_id : int
        profile_pic : str | None
        created_at : date
        profile_pic: Optional[str]


class UserUpdate(UserResponse):
     pass

class Config:
      orm_mode = True


      
