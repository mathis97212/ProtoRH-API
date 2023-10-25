import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture

def create_routes(app, engine):
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
    

    