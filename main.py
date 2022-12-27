"""
main.py is for crating fast api app and connecting db

#running: after activate env, type in terminal :
uvicorn main:app --reload
then in web browser:
http://127.0.0.1:8000/docs for interactive test
"""

# import libs
import model
from database import engine
from fastapi import FastAPI

# instantiate app
app = FastAPI()

# create table
model.Base.metadata.create_all(bind=engine)
