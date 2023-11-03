from sqlalchemy import create_engine, Column, Integer, Float, String, text, Date, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Json
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    password_repeat = Column(String, index=True)
    lastname = Column(String, index=True)
    firstname = Column(String, index=True)
    birthdaydate = Column(String, index=True)
    address = Column(String, index=True)
    postalcode = Column(String, index=True)
    age = Column(Integer)
    meta = Column(JSON)
    registrationdate = (String)
    token = Column(String, index=True)
    role = Column(String, index=True)
    departements = Column(Integer, nullable=True)

class Create(BaseModel):
    email : str
    password : str
    password_repeat : str
    firstname : str
    lastname : str
    birthdaydate : date
    address : str
    postalcode : str

class Update(BaseModel):
    id : int
    name : str
    email : str
    password : str
    firstname : str
    lastname : str
    birthdaydate : date
    address : str
    postalcode : str
    age : int
    meta : str
    registrationdate : date
    token : str
    role : str
    departements : int

class UpdatePassword(BaseModel):
    email : str
    password : str
    new_password : str
    new_password_repeat : str

class UserConnect(BaseModel):
    email : str
    password : str

class GetUser(BaseModel):
    id : int
    name : str
    email : str
    password : str
    firstname : str
    lastname : str
    birthdaydate : date
    address : str
    postalcode : str
    age : int
    meta : str
    registrationdate : date
    token : str
    role : str
    departements : int


class UploadProfilePicture(BaseModel):
    id : int
    token : str
