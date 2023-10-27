import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture
import datetime
import hashlib
import jwt

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
    # this endpoint create a user"
    @app.post("/user/create/")
    async def create_user(user: Create):
        # récupère l'ensemble des paramètres
        values = {
            "email": user.email,
            "password": user.password,
            "password_repeat": user.password_repeat,
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


        # vérifie que le mot de passe repeat correspond bien au mot de passe, si oui je le hash
        if "password" != "password_repeat":
            return {"Please make sure to enter the same password"} 
        else:
            password = "password".encode('utf-8') 
            hash_object = hashlib.md5(password+salt)
            hex_dig = hash_object.hexdigest()
            password_hash = hex_dig

        values = {
            "birthdaydate": user.birthdaydate,
            "registrationdate": user.registrationdate
        }

        # récupère la valeur de l'année de naissance
        birthday_date = values["birthdaydate"]

        #récupère la date actuelle avec la lib datetime
        current_date = datetime.now()

        # calcule l'age à partir de la date de naissance
        age = current_date - birthday_date

        token= 

        # vérifie si un compte n'existe pas déjà avec cet email
        query = text("SELECT email FROM 'User'")
        values = {
            "email": user.email,
        }
        if query == values:
            return {"Account already exists with this email"}
        else:
            values = {
                "email": user.email,
                "password": password_hash,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "birthdaydate": user.birthdaydate,
                "address": user.address,
                "postalcode": user.postalcode,
                "age": age,  
                "meta": JSON{},
                "registrationdate": user.registrationdate,
                "token": user.token,
                "role": user.role 
            }
            
            
            # sauvegarde l'utilisateur dans la base de données
            query = text("INSERT INTO 'User'(email, password, firstname, lastname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role) VALUES (:email, :password, :firstname, :lastname, :birthdaydate, :address, :postalcode, :age, :meta, :registrationdate, :token, :role) RETURNING *")
            with engine.begin() as conn:
                result = conn.execute(query, **values)
                return result.fetchone()