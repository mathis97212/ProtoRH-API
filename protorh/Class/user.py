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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    Email = Column(String, index=True)
    Password = Column(String, index=True)
    Lastname = Column(String, index=True)
    Firstname = Column(String, index=True)
    BirthdayDate = Column(String, index=True)
    Address = Column(String, index=True)
    PostalCode = Column(String, index=True)
    Age = Column(Integer)
    Meta = Column(JSON)
    RegistrationDate = (Integer)
    Token = Column(String, index=True)
    Role = Column(String, index=True)

class Create(BaseModel):
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : date
    Address : str
    PostalCode : int
    Age : int

class Update(BaseModel):
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : date
    Address : str
    PostalCode : int
    Age : int

class UpdatePassword(BaseModel):
    Email : str
    Password : str

class UploadProfilePicture(BaseModel):
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : date
    Address : str
    PostalCode : int
    Age : int
