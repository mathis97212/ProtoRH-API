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
    user_id = Column(Integer)
    content = Column(String)
    registrationdate = Column(Date)
    visibility = Column(Boolean)
    close = Column(Boolean)
    lastaction = Column(Boolean)
    contenthistory = Column(JSON)
    
class CreateRequestRH(BaseModel):
    user_id : int
    content : str
    lastaction : date
    contenthistory : str
    
    
class UpdateRequestRH(BaseModel):
    id : int 
    user_id : int
    Content : str
    registrationdate : date
    visibility : str
    close : str
    lastaction : str
    contenthistory : str

class RemoveRequestRH(BaseModel):
    user_id : int
    content : str
    registrationdate : date
    visibility : str
    close : str
    lastaction : str
    contenthistory : str


class GetRequestRH(BaseModel):
    user_id : int
    content : str
    registrationdate : date
    visibility : str
    close : str
    lastaction : str
    contenthistory : str
