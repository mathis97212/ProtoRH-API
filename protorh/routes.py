import json
import subprocess, uvicorn
from flask import session
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, engine_from_config, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture
import datetime
import hashlib
import jwt
from curses.ascii import isdigit

from dotenv import load_dotenv, dotenv_values

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine_from_config)
Base = declarative_base()

salt = os.getenv("SALT")

# fonction permettant de hasher un mot de passe de type md5 en paramètre
def hash_md5(mdp):
    password = mdp
    salted_password = password + salt
    hash_object = hashlib.md5(salted_password.encode("utf-8"))
    password_hashed = hash_object.hexdigest()
    return password_hashed

def hash_djb2(s):                                                                                                                                
    hash = 5381
    for x in s:
        hash = (( hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF

def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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
        query = text("""
        SELECT email, password, password_repeat, firstname, lastname, birthdaydate, address, postalcode FROM "User"
        """)
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
        with engine.begin() as conn:
            conn.execute(query)

        # vérifie que le mot de passe repeat correspond bien au mot de passe sinon je retourne une erreur
        if values["password"] != values["password_repeat"]:
            return {"Please make sure to enter the same password"}
        # vérifie sur le code postale est bien égale à 5
        elif not user.postalcode.isdigit() and len(values["postalcode"]) != 5:
            return {"Code postale invalide"}
        else:
            mdp = str((values["password"]))
            password_hashed = hash_md5(mdp)

        values = {
            "birthdaydate": user.birthdaydate,
        }

        age = from_dob_to_age(values["birthdaydate"])

        secret_key = os.getenv("SECRET_KEY")

        payload = {
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname
        }

        secret_key = str(secret_key)

        token = jwt.encode(payload, secret_key, algorithm="HS256")+salt

        # vérifie si un compte n'existe pas déjà avec cet email
        query = text("SELECT email FROM 'User'")
        values = {
            "email": user.email,
        }
        if query == values:
            return {"Account already exists with this email"}
        else:
            # sauvegarde l'utilisateur dans la base de données
            query = text(""" INSERT INTO "User" (email, password, firstname, lastname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role, departements) 
                         VALUES (:email, :password, :firstname, :lastname, :birthdaydate, :address, :postalcode, :age, :meta, :registrationdate, :token, :role, :departements) RETURNING *""")

            values = {
                "email": user.email,
                "password": password_hashed,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "birthdaydate": user.birthdaydate,
                "address": user.address,
                "postalcode": user.postalcode,
                "age": from_dob_to_age(values["birthdaydate"]),
                "meta": json.dumps({}),
                "registrationdate": datetime.date.today(),
                "token": hash_djb2(token),
                "role": "user",
                "departements": None
            }
            with engine.begin() as conn:
                conn.execute(query)

