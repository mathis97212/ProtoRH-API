from sqlalchemy import create_engine, Column, Integer, Float, String, text, Date, JSON, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from fastapi import FastAPI
from datetime import date

Base = declarative_base()

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
