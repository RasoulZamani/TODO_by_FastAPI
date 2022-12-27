""" 
auth.py for creating new user and adding it to database
and hashing password by bcrypt 
ant authentication stuff
"""

# import libs _________________________________________________________
import model
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from database import engine, SessionLocal

SECRET_KEY = "ItIsS000Secret!"
ALGORITHM  = "HS256"

app = FastAPI()
# create table if auth run before main
model.Base.metadata.create_all(bind=engine)

# hashing contex
bcrypt_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# jwt 
auth2bearer = OAuth2PasswordBearer(tokenUrl="token")

# authenticate user
def authenticate_user(username: str, password: str, db):
    """ authenticate user"""
    user = db.query(model.User)\
        .filter(model.User.username == username)\
        .first()
    if not user:
        return False
    if not bcrypt_ctx.verify(password, user.hashed_pass):
        return False

    return user 


def get_db():
    """ geeting database either successfully or not and close it """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta]=None):
    """create access json web token"""
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)    
    
    

# base model for user _________________________________________________
class CreateUser(BaseModel):
    """ create base model for user"""
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
       

# html methodes _______________________________________________________
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

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """login for access token"""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, 
                         detail="Oops!User not found or Password is wrong!")
    
    token = create_access_token(user.username, user.id,
                                expires_delta=timedelta(minutes=20))   
    return {"token": token}


# common function for reusing__________________________________________

# successful response
def successful_response(status_code: int):
    """returning dectionary with seccess massage and assosiated code"""
    return {
        "status": status_code,
        "transaction": "Successful"
    } 

      
# exception not found
def not_found_exception():
    """if item in todo table not found, we'll raise exception"""
    return HTTPException(status_code=404, 
                         detail="Oops!not found!")

    