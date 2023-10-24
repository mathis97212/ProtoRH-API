import subprocess
import uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

DATABASE_URL = "postgresql://jawa:123@localhost/ProtoRH"

create = create_engine(DATABASE_URL)
if not database_exists(create.url):
    create_database(create.url, template="template0")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create)
Base = declarative_base()

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
    RegistrationDate: Date
    Visibility: bool
    Close: bool
    LastAction: Date
    ContentHistory: list

class UpdateRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: Date
    Visibility: bool
    Close: bool
    LastAction: Date
    ContentHistory: list

class RemoveRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: Date
    Visibility: bool
    Close: bool
    LastAction: Date
    ContentHistory: list
    
class GetRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: Date
    Visibility: bool
    Close: bool
    LastAction: Date
    ContentHistory: list
