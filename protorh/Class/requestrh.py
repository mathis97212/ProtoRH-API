import subprocess, uvicorn
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, text, Date, JSON, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import date

Base = declarative_base()

class RequestRH(Base):
    __tablename__ = "RequestRH"
    id = Column(Integer, primary_key = True, index=True)
    UserID = Column(Integer)
    Content = Column(String)
    RegistrationDate = Column(Date)
    Visibility = Column(Boolean)
    Close = Column(Boolean)
    LastAction = Column(Boolean)
    ContentHistory = Column(JSON)
    
class CreateRequestRH(BaseModel):
    UserID : int
    Content : str
    RegistrationDate : date
    Visibility : bool
    Close : bool
    LastAction : bool
    ContentHistory : str
    
    
class UpdateRequestRH(BaseModel):
    id : int 
    UserID : int
    Content : str
    RegistrationDate : date
    Visibility : str
    Close : str
    LastAction : str
    ContentHistory : str

class RemoveRequestRH(BaseModel):
    UserID : int
    Content : str
    RegistrationDate : date
    Visibility : str
    Close : str
    LastAction : str
    ContentHistory : str


class GetRequestRH(BaseModel):
    UserID : int
    Content : str
    RegistrationDate : date
    Visibility : str
    Close : str
    LastAction : str
    ContentHistory : str
