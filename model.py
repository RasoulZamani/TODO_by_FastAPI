""" model.py is for creating schema of our database"""

# import libs:
from sqlalchemy import Boolean, Column, String, Integer
from database import Base

# create class of database
class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index = True)
    title = Column( String,)
    description = Column(String, )
    priority = Column(Integer,)
    complete = Column(Boolean, default=False)
    
    