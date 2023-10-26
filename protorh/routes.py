import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture

import hashlib

from dotenv import load_dotenv, dotenv_values

Base = declarative_base

salt = os.getenv("SALT")

def create_routes(app, engine):
    # Endpoint : /
    # Type : GET
    # this endpoint return à json string containing "Hello world !"
    @app.get("/")
    async def read_root():
        return {"Hello world !"}
    
    # Endpoint : /user/create
    # Type : POST
    # this endpoint ..."
    @app.post("/user/create/")
    async def create_user(user= Create):
        query = text("SELECT email, password FROM 'User'")
        values = {
            "email": user.email,
            "password": user.password,
            "password_repeat": user.password_repeat,
        }
        if "password" != "password_repeat":
            return {"Please make sure to enter the same password"} 
        else:
            password = "password".encode('utf-8') 
            hash_object = hashlib.md5(password)
            hex_dig = hash_object.hexdigest() + salt
        
        

        query = text("INSERT INTO 'User'(email, password, firstname, lastname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role) VALUES (:email, :password, :firstname, :lastname, :birthdaydate, :address, :postalcode, :age, :meta, :registrationdate, :token, :role) RETURNING *")
        values = {
            "email": user.email,
            "password": user.password,
            "password": user.password_repeat,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "birthdaydate": user.birthdaydate,
            "address": user.address,
            "postalcode": user.postalcode,
            "age": user.age, 
            "meta": user.meta,
            "registrationdate": user.registrationdate,
            "token": user.token,
            "role": user.role 
        }
        with engine.begin() as conn:
            result = conn.execute(query, **values)
            return result.fetchone()
