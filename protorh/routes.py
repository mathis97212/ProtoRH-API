import json
from flask import session
import os
from fastapi import Depends, HTTPException
from sqlalchemy import text, JSON, URL

from Class.user import User, Create, Update, UpdatePassword,GetUser, UploadProfilePicture, UserConnect
from Class.departement import Department, AddUserToDepartment, RemoveUserFromDepartment, GetUsersInDepartment
from Class.requestrh import RemoveRequestRH, UpdateRequestRH, RequestRH, GetRequestRH
from Class.event import Event, CreateEvent, GetEvent, RemoveEvent

import datetime
import hashlib
import jwt
from curses.ascii import isdigit
from fastapi import APIRouter
from database import get_db
from fastapi.security import OAuth2PasswordBearer

from functools import wraps
from flask import Flask, request, jsonify



engine = get_db()
router = APIRouter()
salt = os.getenv("SALT")

# fonction permettant de hasher un mot de passe de type md5 en paramètre
def hash_md5(mdp):
    password = mdp
    salted_password = password + salt
    hash_object = hashlib.md5(salted_password.encode("utf-8"))
    password_hashed = hash_object.hexdigest()
    return password_hashed

# fonction permettant de hasher un objet de type djb2 en paramètre
def hash_djb2(s):                                                                                                                                
    hash = 5381
    for x in s:
        hash = (( hash << 5) + hash) + ord(x)
    return hash & 0xFFFFFFFF

# fonction permettant qui renvoi l'age à partir de la date de naissance
def from_dob_to_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

secret_key = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from database import SessionLocal
SessionLocal = SessionLocal()
con = SessionLocal
# Fonction pour valider le token JWT
def valide_token(token: str = Depends(oauth2_scheme)):
    try:
        user = con.query(User).filter(User.token == token).first()
        if user:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return user
        else:
            raise HTTPException(status_code=401, detail="Utilisateur non trouvé")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalide")

#--------------------------------------User-------------------------------------#

# Endpoint : /
# Type : GET
# this endpoint return à json string containing "Hello world !"
@router.get("/")
async def read_root():
    return {"Hello world !"}

# Endpoint : /user/create
# Type : POST
# this endpoint create a user
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
            token="",
            role="user",
            departements=None
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            return result

# Endpoint : /connect
# Type : POST
# this endpoint connect to a user
@router.post("/connect/")
async def connect(user: UserConnect):
    query = text("""
        SELECT email, firstname, lastname FROM "Users"
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
        email, firstname, lastname = user_values
        payload = {
            "email": email,
            "firstname": firstname,
            "lastname": lastname
        }
    
        secret_key = os.getenv("SECRET_KEY")
        secret_key = str(secret_key)
        token_unhashed = jwt.encode(payload, secret_key, algorithm="HS256")+salt
        token_hashed = hash_djb2(token_unhashed)

        query = text("""
                    UPDATE "Users"
                    SET token = :token
                    WHERE email = :email 
                    """)
        query = query.bindparams(
            token=token_hashed,
            email=email
        )

        with engine.begin() as conn:
            result = conn.execute(query)

        return {"Connexion réussie": token_hashed}
    else:
        # Sinon si l'utilisateur n'existe pas je renvoye une réponse HTTP 401
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

# Endpoint : /user/{id_user}
# Type : GET
# this endpoint give information about a user
@router.get("/user/{id_user}")
async def info_user(user: GetUser, authorized_user: User = Depends(valide_token)):
    if authorized_user.role == "admin":
        query = text("""
                     SELECT id, name, email, lastname, firstname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role, departements
                     FROM "Users"
                     WHERE id = :id
                     """)
    else:
        query = text("""
                     SELECT id, name, email, lastname, firstname, age, registrationdate, role, departements
                     FROM "Users"
                     WHERE id = :id
                     """)
    query = query.bindparams(
        id=user.id,
        name, 
        email, 
        lastname, 
        firstname, 
        birthdaydate, 
        address, 
        postalcode, 
        age, 
        meta, 
        registrationdate, 
        token, 
        role, 
        departements
        )
    with engine.begin() as conn:
            result = conn.execute(query)
            return result


# Endpoint : /user/update
# Type : POST
# this endpoint update user informations
router.post("/user/update")
async def update_user(Update):
    pass

# Endpoint : /user/password
# Type : POST
# this endpoint update the user password
router.post("/user/password")
async def password_user():
    pass

# Endpoint : /upload/picture/user/{user_id}
# Type : POST
# this endpoint update user informations
router.post("/upload/picture/user/{user_id}")
async def upload_picture_user():
    pass

# Endpoint : /picture/user/{user_id}
# Type : get
# this endpoint recover a user picture
router.get("/picture/user/{user_id}")
async def picture_user():
    pass

#--------------------------------------Departement-------------------------------------#

# Endpoint : /departements/{id_departement}/users/add
# Type : POST
# this endpoint add users defined to a group
router.post("/departements/{id_departement}/users/add")
async def add_user():
    pass

# Endpoint : /departements/{id_departement}/users/remove
# Type : POST
# this endpoint remove users defined to a group
router.post("/departements/{id_departement}/users/remove")
async def remove_user():
    pass

# Endpoint : /departements/{id_departement}/users
# Type : GET
# this endpoint retrieves users from a group
router.get("/departements/{id_departement}/users")
async def remove_user():
    pass

#--------------------------------------RequestRH-------------------------------------#

# Endpoint : /rh/msg/add
# Type : POST
# this endpoint create an RH request
router.post("/rh/msg/add")
async def create_request():
    pass

# Endpoint : /rh/msg/remove
# Type : POST
# this endpoint remove an RH request
router.post("/rh/msg/remove")
async def remove_request():
    pass

# Endpoint : /rh/msg/update
# Type : POST
# this endpoint update an RH request
router.post("/rh/msg/update")
async def update_request():
    pass

# Endpoint : /rh/msg
# Type : GET
# this endpoint retrieves HR requests
router.get("/rh/msg")
async def retrieval_request():
    pass

#--------------------------------------Event-------------------------------------#

# Endpoint : /event/add
# Type : POST
# this endpoint add an evenement
router.post("/event/add")
async def add_event():
    pass

# Endpoint : /event/add
# Type : GET
# this endpoint retrievies event(s)
router.get("/event")
async def retrievial_event():
    pass

# Endpoint : /event/remove
# Type : POST
# this endpoint remove an event
router.get("event/remove")
async def remove_event():
    pass

