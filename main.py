"""
main.py is for crating fast api app and connecting db

#running: after activate env, type in terminal :
uvicorn main:app --reload
then in web browser:
http://127.0.0.1:8000/docs for interactive test
"""

# import libs
import model
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import Optional
 


# instantiate app
app = FastAPI()

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
@app.get('/')
async def read_all_list(db: Session=Depends(get_db)):
    """first get database and then reading all jobs in todo table """ 
    return db.query(model.Todo).all()


# read data with specified id _________________________________________
@app.get("/todo/{todo_id}")
async def read_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    """first get database and then read data with specified id"""
    result = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .first()
    if result is not None:
        return result
    raise not_found_exception()


# post new todo item __________________________________________________ 
@app.post("/")
async def create_todo_item(todo: Todo, db: Session = Depends(get_db)):
    """after connecting to db, create todo item and adding to db"""
    todo_model = model.Todo()
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
    return {
        "status": 201,
        "transaction": "Successful"
    }
    
 
# put (update) item with specified id
@app.put("/{todo_id}")
async def update_item(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    """after connecting to db, updating todo item"""
    todo_model = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .first()
    if todo_model is None:
        raise not_found_exception()
    
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.add(todo_model)
    db.commit()
    
    return {
        "status": 200,
        "update": "Successful"
    }
     
     
 
# delete item with specified id
@app.delete("/{todo_id}")
async def delete_item(todo_id: int, db: Session = Depends(get_db)):
    """after connecting to db, delete todo item"""
    todo_model = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .first()
    if todo_model is None:
        raise not_found_exception()
    
    db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .delete()
        
    db.commit()
    
    return {
        "status": 201,
        "update": "Successful"
    } 
    
# exception not found
def not_found_exception():
    """if item in todo table not found, we'll raise exception"""
    return HTTPException(status_code=404, 
                         detail="Oops! Todo item not found!")
