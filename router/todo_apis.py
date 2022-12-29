"""
todo_apis.py is for crating fast api todo app 

"""
# import libs
import sys
sys.path.append("..") # adding parent folder to path

import model
from database import engine, SessionLocal
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
from .auth import get_current_user, token_exception


# instantiate routerr
router = APIRouter(
    prefix="/todo",
    tags=["ToDo APIs"],
    responses={"404":{"description":"Not Found"}}
    
)
# create table
model.Base.metadata.create_all(bind=engine)

def get_db():
    """ geeting database either successfully or not and close it """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        

class Todo(BaseModel):
    """base model for items in db"""
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description="the priority must be between 1-5")
    complete: bool
        
# read all data _______________________________________________________
@router.get('/')
async def read_all_list(db: Session=Depends(get_db)):
    """first get database and then reading all jobs in todo table """ 
    return db.query(model.Todo).all()

# read todo list of autenticated user__________________________________
@router.get("/user")
async def read_all_todo_by_user(user: dict = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    """read all todo by user"""
    if user is None:
        raise token_exception()
    return db.query(model.Todo)\
        .filter(model.Todo.owner_id == user.get("id"))\
        .all() 
        
        
# read data with specified id _________________________________________
@router.get("/{todo_id}")
async def read_todo_by_id(todo_id: int,
                          user: dict = Depends(get_current_user),
                          db: Session = Depends(get_db)):
    """first get database and then read data with specified id"""
    if user is None:
        raise token_exception()
    result = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .filter(model.Todo.owner_id == user.get("id"))\
            .first()
    if result is not None:
        return result
    raise not_found_exception()


# post new todo item __________________________________________________ 
@router.post("/")
async def create_todo_item(todo: Todo,
                           user: dict = Depends(get_current_user),
                           db: Session = Depends(get_db)):
    """after connecting to db, create todo item and adding to db"""
    if user is None:
        raise token_exception()
    
    todo_model = model.Todo()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    todo_model.owner_id = user.get("id")
    
    db.add(todo_model)
    db.commit()
    
    return successful_response(201)
    
 
# put (update) item with specified id
@router.put("/{todo_id}")
async def update_item(todo_id: int,
                      todo: Todo,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """after connecting to db, updating todo item"""
    
    if user is None:
        raise token_exception()
    
    todo_model = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .filter(model.Todo.owner_id == user.get("id"))\
            .first()
            
    if todo_model is None:
        raise not_found_exception()
    
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
    return successful_response(200)
     
      
# delete item with specified id _______________________________________
@router.delete("/{todo_id}")
async def delete_item(todo_id: int,
                      user: dict = Depends(get_current_user),
                      db: Session = Depends(get_db)):
    """after connecting to db, delete todo item"""
    
    if user is None:
        raise token_exception()
    
    todo_model = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .filter(model.Todo.owner_id == user.get("id"))\
            .first()
             
    if todo_model is None:
        raise not_found_exception()
    
    db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .delete()
        
    db.commit()
    
    return successful_response(201)
    
    
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
                         detail="Oops! Todo item not found!")
