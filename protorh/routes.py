import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture
from datetime import datetime
import hashlib
import jwt
from curses.ascii import isdigit

from dotenv import load_dotenv, dotenv_values

Base = declarative_base

salt = os.getenv("SALT")

# fonction permettant de hasher un mot de passe de type md5 en paramètre
def hash_password(mdp, salt):
    password = mdp.encode('utf-8')
    salted_password = password + salt
    hash_object = hashlib.md5(salted_password)
    password_hashed = hash_object.hexdigest()
    
    return password_hashed

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
        }

        # vérifie que le mot de passe repeat correspond bien au mot de passe, si oui je le hash
        if values["password"] != values["password_repeat"]:
            return {"Please make sure to enter the same password"}
        elif not user.postalcode.isdigit() and len(values["postalcode"]) != 5:
            return {"Code postale invalide"}
        else:
            password_hashed = hash_password(values["password"], salt)

        values = {
            "birthdaydate": user.birthdaydate,
            "registrationdate": user.registrationdate
        }

        # récupère la valeur de l'année de naissance
        birthday_date = values["birthdaydate"]

        #récupère la date actuelle avec la lib datetime
        current_date = datetime.now()

        # calcule l'age à partir de la date de naissance
        age = current_date[:4] - birthday_date[:4]

        secret_key = os.getenv("SECRET_KEY")

        payload = {
            "email": values["email"],
            "firstname": values["firstname"],
            "lastname": values["lastname"]
        }

        token = jwt.encode(payload, secret_key, algorithm="HS256")+salt

        token_to_hash = token.encode('utf-8') 
        hash_object = hashlib.djb2(token_to_hash)
        hex_dig = hash_object.hexdigest()
        token_hashed = hex_dig

        meta = []

        registrationdate = datetime.now()

        departements = None

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
                "password": password_hashed,
                "password_repeat": password_hashed,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "birthdaydate": user.birthdaydate,
                "address": user.address,
                "postalcode": user.postalcode,
                "age": age,  
                "meta": meta,
                "registrationdate": registrationdate,
                "token": token_hashed,
                "role": user,
                "departements": departements
            }
            
            # sauvegarde l'utilisateur dans la base de données
            query = text("INSERT INTO 'User'(email, password, firstname, lastname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role) VALUES (:email, :password, :firstname, :lastname, :birthdaydate, :address, :postalcode, :age, :meta, :registrationdate, :token, :role) RETURNING *")
            with engine.begin() as conn:
                result = conn.execute(query, **values)
                return result.fetchone()