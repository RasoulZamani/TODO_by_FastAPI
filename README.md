# TODO App by FastAPI

This is a simple educational web app by **FastAPI**

After connecting to **sqlite** database by **SQLalchemy (ORM)**,**CRUD** methodes (create, read, update and delete) was implemented

user and todo tables and also one-to-many relationship between them (by ForeignKey) is implemented  
**JWT** (json web token) is used for authentication


# requirements
install these libs in your system (virtual environment recomended):

```


```

# run
first cloning this repo and go to directory.
after activating venv, , type in terminal :
`uvicorn main:app --reload`

then in web browser:
`http://127.0.0.1:8000/docs` for interactive test by swagger

