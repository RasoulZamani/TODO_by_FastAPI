""" 
auth.py for creating new user and adding it to database
and hashing password by bcrypt 
ant authentication stuff

 by routing, after running main, this file run automaticly too.
"""

# import libs _________________________________________________________
import sys
sys.path.append("..") # adding parent folder to path
import model
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from database import engine, SessionLocal

# constansts for cryption of pass
SECRET_KEY = "ItIsS000Secret!"
ALGORITHM  = "HS256"

# router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={"401":{"User":"Unseccessful user authentication"}}
)

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
    
    
async def get_current_user(token:str = Depends(auth2bearer)):
    """ get username and id from current user jwt"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        user_id: int  = payload.get("id")
        if username is None or user_id is None:
            raise user_exception()
        
        return {"username":username, "id": user_id}
        
    except JWTError:
        raise token_exception()

# base model for user _________________________________________________
class CreateUser(BaseModel):
    """ create base model for user"""
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
       

# html methodes _______________________________________________________
@router.post("/create/user")
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

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    """login for access token"""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise user_exception()
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

      
# get token_exception
def token_exception():
    """get token exception"""
    token_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"}
        )
    return token_exc

# get user exception
def user_exception():
    """get user exception"""
    credetials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username!",
        headers={"WWW-Authenticate": "Bearer"}
        )
    return credetials_exc
 