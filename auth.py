""" 
auth.py for creating new user
and hashing password by bcrypt 
ant authentication stuff
"""

# import libs _________________________________________________________
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
import model

# base model for user _________________________________________________
class CreateUser(BaseModel):
    """ create base model for user"""
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str

# hashing contex
bcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
 
app = FastAPI()

@app.post("/create/user")
async def create_new_user(create_user: CreateUser):
    """creating new user"""
    create_user_model = model.User()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.hashed_pass = bcrypt_ctx.hash(create_user.password) 
    create_user_model.is_active = True
    
    return create_user_model
    