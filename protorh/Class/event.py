import subprocess, uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text, engine, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

Base = declarative_base

class Event(Base):
    __tablename__ = "Event"
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
    Date = Column(Integer, index=True)
    Description = Column(String, index=True)
    UserID = Column(Integer, index=True)
    DepartmentID = Column(Integer, index=True)

class CreateEvent(BaseModel):
    id : int
    Name : str 
    Date : int 
    Description : str
    UserID : int
    DepartmentID : int
class GetEvent(BaseModel):
    id : int
    Name : str 
    Date : int 
    Description : str
    UserID : int
    DepartmentID : int
class RemoveEvent(BaseModel):
    id : int
    Name : str 
    Date : int 
    Description : str
    UserID : int
    DepartmentID : int
