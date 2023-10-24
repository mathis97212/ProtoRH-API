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
Base = declarative_base

class Department(Base):
    __tablename__ = "Department"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
class AddUserToDepartment(BaseModel):
    __tablename__ = "AddUserToDepartment"
    id : int
    name : str
class RemoveUserFromDepartment(BaseModel):
    __tablename__ = "RemoveUserFromDepartment"
    id : int
    name : str
class GetUsersInDepartment(BaseModel):
    __tablename__ = "GetUsersInDepartment"
    id : int
    name : str


