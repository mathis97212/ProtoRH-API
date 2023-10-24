import subprocess, uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

DATABASE_URL = "postgresql://jawa:123@localhost/ProtoRH"

create = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url, template="template0")

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
base = declarative_base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    Email = Column(String, index=True)
    Password = Column(String, index=True) #Hashed
    Lastname = Column(String, index=True)
    Firstname = Column(String, index=True)
    BirthdayDate = Column(String, index=True)
    Address = Column(String, index=True)
    PostalCode = Column(String, index=True)
    Age = Column(Integer)
    Meta = Column(JSON)
    RegistrationDate = (Integer)
    Token = Column(String, index=True) #Hashed
    Role = Column(String, index=True)

class Create(BaseModel):
    __tablename__ = "creates"
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : int
    Address : str
    PostalCode : int
    Age : int

class Update(BaseModel):
    __tablename__ = "updates"
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : int
    Address : str
    PostalCode : int
    Age : int
