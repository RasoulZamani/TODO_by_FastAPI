""" 
auth.py for creating new user and adding it to database
and hashing password by bcrypt 
ant authentication stuff
"""

# import libs _________________________________________________________
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from database import engine, SessionLocal
import model

# hashing contex
bcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
app = FastAPI()
# create table if auth run before main
model.Base.metadata.create_all(bind=engine)


def get_db():
    """ geeting database either successfully or not and close it """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# base model for user _________________________________________________
class CreateUser(BaseModel):
    """ create base model for user"""
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
       

@app.post("/create/user")
async def create_new_user(create_user: CreateUser, db: Session=Depends(get_db)):
    """creating new user"""
    create_user_model = model.User()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.hashed_pass = bcrypt_ctx.hash(create_user.password) 
    create_user_model.is_active = True
    
    db.add(create_user_model)
    db.commit()
    
    return successful_response(200)
    
    
    

# successful response
def successful_response(status_code: int):
    """returning dectionary with seccess massage and assosiated code"""
    return {
        "status": status_code,
        "transaction": "Successful"
    } 
    