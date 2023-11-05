import json
from flask import session
import os
from fastapi import Depends, HTTPException, Path, Form, File, UploadFile
from sqlalchemy import text, JSON, URL
from PIL import Image

from Class.user import User, Create, Update, UpdatePassword,GetUser, UploadProfilePicture, UserConnect
from Class.departement import Department, AddUserToDepartment, RemoveUserFromDepartment, GetUsersInDepartment
from Class.requestrh import RemoveRequestRH, UpdateRequestRH, RequestRH, GetRequestRH
from Class.event import Event, CreateEvent, GetEvent, RemoveEvent

import datetime
import hashlib
import jwt
from env import getenv
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

# Fonction pour valider le token JWT
def valide_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token expiré"
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )

    return True

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
@router.post("/user/create/", status_code=201)
async def create_user(user: Create):
    # vérifie que le mot de passe repeat correspond bien au mot de passe sinon je retourne une erreur
    if user.password != user.password_repeat:
        return HTTPException(400, {"error": "Please make sure to enter the same password"})
    # vérifie sur le code postale est bien égale à 5
    elif not user.postalcode.isdigit() and len(user.postalcode) != 5:
        return HTTPException(400, {"error": "Invalid postalcode"})
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
        payload = {
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname
        }

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
            token="", #hash(payload+salt),
            role=user.role,
            departements=None
        )

        with engine.begin() as conn:
            result = conn.execute(query)
            return {"User created"}

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
    
        secret_key = getenv("SECRET_KEY")
        secret_key = str(secret_key)
        token_unhashed = jwt.encode(payload, secret_key, algorithm="HS256")
        token_hashed = (token_unhashed)

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

        return {"Successful connection": token_hashed}
    else:
        # Sinon si l'utilisateur n'existe pas je renvoye une réponse HTTP 401
        raise HTTPException(status_code=401, detail="incorrect credentials")

# Endpoint : /user/{id}
# Type : GET
# this endpoint give information about a user
@router.get("/user/{id_user}")
async def info_user(id_user: int, valid_token: bool = Depends(valide_token)):
    query = text("""
                     SELECT id, email, lastname, firstname, birthdaydate, address, postalcode, age, meta, registrationdate, token, role, departements FROM "Users"
                     WHERE id = :id
                     """)
    values = {
            "id" : id_user
    }
    with engine.begin() as conn:
            result = conn.execute(query, values)
            user_values = result.fetchone()

    if user_values[11] == 'admin':
        return {user_values[0], user_values[1], user_values[2], user_values[5], user_values[6], user_values[7], user_values[8], user_values[9], user_values[10], user_values[11], user_values[12], user_values[13], user_values[14], user_values[15]}
    else:
        return {user_values[0], user_values[1], user_values[2], user_values[5], user_values[6], user_values[10], user_values[12], user_values[14], user_values[15]}
                
# Endpoint : /user/update
# Type : POST
# this endpoint update user informations
router.post("/user/update")
async def update_user(user: Update):
    if user.role == "admin":
        query = text("""
                    UPDATE "Users"
                    SET name = :name, email = :email, lastname = :lastname, firstname = :firstname, birthdaydate = :birthdaydate, address = :address, postalcode = :postalcode, age = :age, meta = :meta, registrationdate = :registrationdate, role = :role, departements = :departements
                    WHERE id = :id 
                     """)
    else:
        query = text("""
                    UPDATE "Users"
                    SET name = :name, email = :email, birthdaydate = :birthdaydate, address = :address, postalcode = :postalcode, age = :age, meta = :meta, registrationdate = :registrationdate, departements = :departements
                    WHERE id = :id
                     """)
    query = query.bindparams(
        id=user.id,
        name=user.name, 
        email=user.email, 
        lastname=user.lastname, 
        firstname=user.firstname, 
        birthdaydate=user.birthdaydate, 
        address=user.address, 
        postalcode=user.postalcode, 
        age=user.age, 
        meta=user.meta, 
        registrationdate=user.registrationdate, 
        token=user.token, 
        role=user.role, 
        departements=user.departements
        )
    with engine.begin() as conn:
            result = conn.execute(query)
            user_values = result.fetchone()
    if user_values:
        return {"Successful update"}
    else:
        HTTPException(status_code=401, detail="Update failed")

# Endpoint : /user/password
# Type : POST
# this endpoint update the user password
router.post("/user/password")
async def password_user(user : UpdatePassword):

    query = text("""
                SELECT password FROM "Users"
                WHERE email = :email
                """)
    values = {"email": user.email}
    with engine.begin() as conn:
            result = conn.execute(query, values)
            existing_password = result.fetchone() 

    if existing_password:
        if hash_md5(user.password) == existing_password: 
            if user.new_password != user.new_password_repeat:
                return {"Please make sure to enter the same password"} 
            else:
                query = text("""
                            UPDATE "Users"
                            SET password = :password
                            WHERE email = :email
                            """)
                query = query.bindparams(
                    password = hash_md5(user.new_password)
                    )
                with engine.begin() as conn:
                        result = conn.execute(query)
                        existing_email_password = result.fetchone()
        else:
            return {"error": "User email not found"}
    

# Endpoint : /upload/picture/user/{user_id}
# Type : POST
# this endpoint upload a picture
router.post("/upload/picture/user/{user_id}")
async def upload_picture_user(user: UploadProfilePicture, image: UploadFile = File(...)):

    query = text("""
                SELECT token FROM "Users"
                WHERE id = :id
                 """)
    
    values = {
            "id" : user.id
            }

    with engine.begin as conn:
        result = conn.execute(query, values)
        existing_token = result.fetchone()
    
    if existing_token:
        # Vérification de la taille et du format de l'image.
        allowed_extensions = {'jpg','png', 'gif'}
        
        if image.content_type.split('/')[1] in allowed_extensions:
            img = Image.open(image.file)
            largeur, hauteur = img.size

            if largeur <= 800 and hauteur <= 800:
                file_extension = image.filename.split('.')[-1]
                file_name = f"{existing_token}.{file_extension}"
                file_path = f"assets/picture/profiles/{file_name}"

                with open(file_path, 'wb') as f:
                    f.write(image.file.read())

                return {"Image uploaded successfully."}
            else:
                return {type: "upload_error", "error": "Image size exceeds the limit (800x800)."}
        else:
            return {type: "upload_error", "error": "Invalid image format. Allowed formats: jpg, jpeg, png, gif."}
    else:
        return {type: "user_error", "error": "User not found"}
        
    

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

