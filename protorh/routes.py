import json
import subprocess, uvicorn
from flask import session
import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, engine_from_config, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from Class.user import User, Create, Update, UpdatePassword,GetUser, UploadProfilePicture
import datetime
import hashlib
import jwt
from curses.ascii import isdigit
from fastapi import APIRouter
from database import get_db

engine = get_db()
router = APIRouter()

salt = os.getenv("SALT")
print(salt)

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

# Endpoint : /
# Type : GET
# this endpoint return à json string containing "Hello world !"
@router.get("/")
async def read_root():
    return {"Hello world !"}

# Endpoint : /user/create
# Type : POST
# this endpoint create a user"
@router.post("/user/create/")
async def create_user(user: Create):
    # vérifie que le mot de passe repeat correspond bien au mot de passe sinon je retourne une erreur
    if user.password != user.password_repeat:
        return {"Please make sure to enter the same password"}
    # vérifie sur le code postale est bien égale à 5
    elif not user.postalcode.isdigit() and len(user.postalcode) != 5:
        return {"Code postale invalide"}
    else:
        mdp = str((user.password))
        password_hashed = hash_md5(mdp)

    secret_key = os.getenv("SECRET_KEY")

    payload = {
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname
    }

    secret_key = str(secret_key)
    token = jwt.encode(payload, secret_key, algorithm="HS256")+salt

    # vérifie si un compte n'existe pas déjà avec cet email
    query = text("""
                SELECT email FROM "Users"
                WHERE email = :email
            """)
    values = {
        "email": user.email
    }
    with engine.begin() as conn:
        result = conn.execute(query, values)
        existing_email = result.fetchone()

    # Check if the email exists in the database
    if existing_email:
        raise HTTPException(status_code=409, detail="An account already exists with this email")
    else:
        # sauvegarde l'utilisateur dans la base de données
        query = text("""
            INSERT INTO "Users" (email, password, password_repeat, firstname, lastname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role, departements) 
            VALUES (:email, :password, :password_repeat, :firstname, :lastname, :birthdaydate, :address, :postalcode, :age, :meta, :registrationdate, :token, :role, :departements) RETURNING *
        """)

        query = query.bindparams(
            email=user.email,
            password=password_hashed,
            password_repeat=password_hashed,
            firstname=user.firstname,
            lastname=user.lastname,
            birthdaydate=user.birthdaydate,
            address=user.address,
            postalcode=user.postalcode,
            age=from_dob_to_age(user.birthdaydate),
            meta=json.dumps({}),
            registrationdate=datetime.date.today(),
            token=hash_djb2(token),
            role="user",
            departements=None
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            return result

# Endpoint : /connect
# Type : POST
# this endpoint connect to a user"
@router.post("/connect/")
async def connect(user: GetUser):
    query = text("""
        SELECT token FROM "Users"
        WHERE email = :email AND password = :password
    """)

    values = {
        "email": user.email,
        "password": hash_md5(str(user.password))
    }

    with engine.begin() as conn:
        result = conn.execute(query, values)
        user_values = result.fetchone()

    if user_values:
        # Si l'utilisateur existe
        token = user_values[0] 
        return {"Connexion réussie": token}
    else:
        # Sinon si l'utilisateur n'existe pas je renvoie une réponse HTTP 401
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
    



