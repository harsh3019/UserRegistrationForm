from fastapi import FastAPI,APIRouter,Form,UploadFile,File,Depends,HTTPException
from schemas.user_schemas import UserResponse,UserUpdate
from models.user_models import Users
from datetime import date
import os
from sqlalchemy.orm import Session
from config.db import get_db
from uuid import uuid4
import random

userapi = APIRouter()

#Directory to store uplod Image
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER,exist_ok = True)

def random_generate_id():
 return random.randint(1000,9999)



#add data to database
@userapi.post('/user/add',response_model=UserResponse)
async def useradd(
    name : str = Form(...),
    age : int = Form(...),
    address : str = Form(...),
    school_name : str = Form(...),
   # unique_id : int = Form(...),
    created_at : date = Form(...),
    profile_pic : UploadFile = File(...),
    db : Session = Depends(get_db)
):
    #save file and Image to the upload directory and Database
    file_extension = os.path.splitext(profile_pic.filename)[1]

    if file_extension not in  [".jpg",".png",".jpeg",".pdf",".doc"]:
        raise HTTPException(status_code=400, details="File Not Supported or Invalid file Format")
    
    filename  =  f"{uuid4()}{file_extension}"
    filepath = os.path.join(UPLOAD_FOLDER,filename)
    with open(filepath, "wb") as buffer:
        buffer.write(profile_pic.file.read())

    unique_id = random_generate_id()
    #save metadata to database
    db_insert = Users(name = name,
                      age = age, 
                      address = address,
                      school_name = school_name,
                      unique_id = unique_id,
                      created_at =created_at,
                      profile_pic = filename)
    db.add(db_insert)
    db.commit()
    db.refresh(db_insert)
    return db_insert


@userapi.get('/get/userdata/{id}',response_model=UserResponse)
async def get_user_details(id:int,db:Session =Depends(get_db)):
   db_data = db.query(Users).filter(Users.id == id).first()
   if not db_data:
      raise HTTPException(status_code=404,detail="User not found")
   return db_data


@userapi.get('/all/data', response_model=list[UserResponse])
async def userdetails(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    db_users = db.query(Users).offset(skip).limit(limit).all()
    return db_users

@userapi.put('/user/update/{id}', response_model=UserUpdate)
async def update_user_info(
    id: int,
    name: str = Form(...),
    age: int = Form(...),
    address: str = Form(...),
    school_name: str = Form(...),
    profile_pic: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Fetch existing user
    db_update_data = db.query(Users).filter(Users.id == id).first()

    if not db_update_data:
        raise HTTPException(status_code=404, detail="User Details not found")

    # Update file if provided
    if profile_pic:
        file_extension = os.path.splitext(profile_pic.filename)[1]

        if file_extension not in [".jpg", ".png", ".jpeg", ".pdf", ".doc"]:
            raise HTTPException(status_code=400, detail="File Not Supported or Invalid file Format")

        filename = f"{uuid4()}{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Save new file
        with open(filepath, "wb") as buffer:
            buffer.write(profile_pic.file.read())

        # Remove old file if it exists
        if db_update_data.profile_pic and os.path.exists(os.path.join(UPLOAD_FOLDER, db_update_data.profile_pic)):
            os.remove(os.path.join(UPLOAD_FOLDER, db_update_data.profile_pic))

        # Update the file name in the user record
        db_update_data.profile_pic = filename

    # Update other fields
    db_update_data.name = name
    db_update_data.age = age
    db_update_data.address = address
    db_update_data.school_name = school_name

    # Commit changes
    db.add(db_update_data)
    db.commit()
    db.refresh(db_update_data)

    return db_update_data


#Delete the User

@userapi.delete('/user/delete/{id}', response_model=UserResponse)
async def delete_user(id: int, db: Session = Depends(get_db)):
    # Fetch the user record
    db_delete_data = db.query(Users).filter(Users.id == id).first()

    if not db_delete_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove the profile picture from the upload folder if it exists
    if db_delete_data.profile_pic and os.path.exists(os.path.join(UPLOAD_FOLDER, db_delete_data.profile_pic)):
        os.remove(os.path.join(UPLOAD_FOLDER, db_delete_data.profile_pic))

    # Delete the user record from the database
    db.delete(db_delete_data)
    db.commit()

    return db_delete_data





