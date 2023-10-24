import subprocess, uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from user import User, Create, Update, UpdatePassword, UploadProfilePicture

DATABASE_URL = "postgresql://jawa:123@localhost/ProtoRH"

create = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url, template="template0")

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base

app = FastAPI()

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
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : int
    Address : str
    PostalCode : int
    Age : int

class Update(BaseModel):
    Email : str
    Password : str
    Firstname : str
    Lastname : str
    BirthdayDate : int
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
    BirthdayDate : int
    Address : str
    PostalCode : int
    Age : int

@app.post("/user/create/", response_model=User)
async def create_user(user: User):
    query = text("INSERT INTO User (Email, Password, Firstname, Lastname, BirthdayDate, Address, PostalCode) VALUES (:Email, :Password, :Firstname, :Lastname, :BirthdayDate, :Address, :PostalCode) RETURNING *")
    values = {
        "Email":user.Email,
        "Password":user.Password,
        "Firstname":user.Firstname,
        "Lastname":user.Lastname,
        "BirthdayDate":user.BirthdayDate,
        "Address":user.Address,
        "PostalCode":user.PostalCode
    }
    with engine.begin() as conn:
        result = conn.execute(query, **values)
        return result.fetchone()

@app.post("/connect/", response_model=User)
async def connect_user(user: User):
    query = text("INSERT INTO User (Email, Password, Firstname, Lastname, BirthdayDate, Address, PostalCode) VALUES (:Email, :Password, :Firstname, :Lastname, :BirthdayDate, :Address, :PostalCode) RETURNING *")
    values = {
        "Email":user.Email,
        "Password":user.Password
    }
    with engine.begin() as conn:
        result = conn.execute(query, **values)
        return result.fetchone()
    