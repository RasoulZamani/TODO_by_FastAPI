""" user_apis.py is for api asosiated to uset in ToDo app"""


# import libs _________________________________________________________
import sys
sys.path.append("..") # adding parent folder to path
import model
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import engine, SessionLocal
from .auth import get_current_user, token_exception, user_exception, bcrypt_ctx

# create table
model.Base.metadata.create_all(bind=engine)

# router
router = APIRouter(
    prefix="/user",
    tags=["Users APIs"],
    responses={"401":{"User":"Not Found"}}
)

def get_db():
    """ geeting database either successfully or not and close it """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerify(BaseModel):
    """base model for update password"""
    username: str
    password: str
    new_password: str

# read all users _______________________________________________________
@router.get('/all')
async def read_all_list(db: Session=Depends(get_db)):
    """first get database and then reading all users in table """ 
    return db.query(model.User).all()
 
 # read data with specified id (path param)____________________________
@router.get("/{user_id}")
async def read_user_in_path_by_id(user_id: int,
                          db: Session = Depends(get_db)):
    """first get database and then read data with specified id as path param"""

    result = db.query(model.User)\
            .filter(model.User.id == user_id)\
            .first()
    if result is not None:
        return result
    raise "invalid User ID"

 # read data with specified id (query method)__________________________
@router.get("/")
async def read_user_by_id_query(user_id: int,
                          db: Session = Depends(get_db)):
    """first get database and then read data with specified id (query method)"""

    result = db.query(model.User)\
            .filter(model.User.id == user_id)\
            .first()
    if result is not None:
        return result
    raise "invalid User ID"

# update password _____________________________________________________
@router.put("/new_password")
async def user_password_change(
    user_verify: UserVerify,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ changing password of user """
    if user is None:
        raise user_exception()
    user_model = db.query(model.User)\
            .filter(model.User.id == user.get("id"))\
            .first()
    if user_model is not None:
        if user_verify.username == user_model.username \
            and bcrypt_ctx.verify(user_verify.password, user_model.hashed_pass):
                user_model.hashed_pass = bcrypt_ctx.hash(user_verify.new_password)
                db.add(user_model)
                db.commit()
                return "Password Updated Successfuly"
    return "Invalid Request"

# delete user _____________________________________________________
@router.delete("/del")
async def delete_user(user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)
):
    """ deleting user """
    if user is None:
        raise user_exception()
    user_model = db.query(model.User)\
            .filter(model.User.id == user.get("id"))\
            .first()
    if user_model is None:
        return "Invalid Request"
    db.query(model.User)\
            .filter(model.User.id == user.get("id"))\
            .delete()
    db.commit()
    
    return "User Deleted Successfuly"