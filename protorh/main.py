import subprocess, uvicorn
<<<<<<< HEAD
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

from Class import user, departement, event, requestrh

from dotenv import load_dotenv, dotenv_values
import hashlib

Base = declarative_base

salt = os.getenv("salt")

DATABASE_URL = "postgresql://:123@localhost/ProtoRH"

create = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url, template="template0")

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base

app = FastAPI()

# Endpoint : /
# Type : GET
# this endpoint return à json string containing "Hello world !"
@app.get("/")
async def read_root():
    return {"Hello world !"}

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
    
=======
from sqlalchemy import create_engine
>>>>>>> refs/remotes/origin/Ilyes
