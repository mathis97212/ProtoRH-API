import subprocess, uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text, engine, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

Base = declarative_base

class RequestRH(Base):
    __tablename__ = "Event"
    id = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer, index=True)
    Content = Column(String, index=True)
    RegistrationDate = Column(Date, index=True)
    Visibility = Column(Boolean, index=True)
    Close = Column(Boolean, index=True)
    LastAction = Column(Date, index=True)
    ContentHistory = Column(JSON, index=True)

class CreateRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: int
    Visibility: bool
    Close: bool
    LastAction: int
    ContentHistory: list

class UpdateRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: int
    Visibility: bool
    Close: bool
    LastAction: Date
    ContentHistory: list

class RemoveRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: int
    Visibility: bool
    Close: bool
    LastAction: int
    ContentHistory: list
    
class GetRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: int
    Visibility: bool
    Close: bool
    LastAction: int
    ContentHistory: list
