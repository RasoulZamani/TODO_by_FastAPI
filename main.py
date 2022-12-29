"""
main.py is for to do app contains router for auth and apis

#running: after activate env, type in terminal :
uvicorn main:app --reload
then in web browser:
http://127.0.0.1:8000/docs for interactive test
"""

# import libs
import model
from database import engine
from fastapi import FastAPI, Depends

from router import auth, todo_apis, user_apis
from company_api import company_api, dependencies

from starlette.staticfiles import StaticFiles


# instantiate app
app = FastAPI()

# create table
model.Base.metadata.create_all(bind=engine)

# add static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# add rout of auth
app.include_router(auth.router)

# add rout of todo apis 
app.include_router(todo_apis.router)

# add rout of user apis 
app.include_router(user_apis.router)

# external rout to company api
app.include_router(company_api.router,
                   prefix="/company",
                   tags=["Company API"],
                   dependencies=[Depends(dependencies.get_token_header)]
                   )