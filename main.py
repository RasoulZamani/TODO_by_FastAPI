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
        
# read all data
@app.get('/')
async def read_all_list(db: Session=Depends(get_db)):
    """first get database and then reading all jobs in todo table """ 
    return db.query(model.Todo).all()


# read data with specified id
@app.get("/todo/{todo_id}")
async def read_todo_by_id(todo_id: int, db: Session = Depends(get_db)):
    """first get database and then read data with specified id"""
    result = db.query(model.Todo)\
            .filter(model.Todo.id == todo_id)\
            .first()
    if result is not None:
        return result
    raise not_found_exception()



def not_found_exception():
    """if item in todo table not found, we'll raise exception"""
    return HTTPException(status_code=404, 
                         detail="Oops! Todo item not found!")
