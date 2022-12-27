""" 
model.py is for creating schema of our database
one-to-many relationship between user and todo is implemented
"""

# import libs:
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# create class model for user table
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_pass = Column(String)
    is_active = Column(Boolean, default=True)
    
    todo = relationship("Todo", back_populates="owner")
    

# create class model for todo table
class Todo(Base):
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True, index=True)
    title = Column( String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey("user.id"))
    
    owner = relationship("User", back_populates="todo")
    
    