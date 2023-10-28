import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

from Class.departement import Department, AddUserToDepartment, RemoveUserFromDepartment, GetUsersInDepartment
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture
from Class.requestrh import RemoveRequestRH, UpdateRequestRH, RequestRH, GetRequestRH
from Class.event import Event, CreateEvent, GetEvent, RemoveEvent

from routes import create_routes

import routes

import hashlib

from dotenv import load_dotenv, dotenv_values

Base = declarative_base

salt = os.getenv("SALT")

url_object = URL.create(
    "postgresql",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    database=os.getenv("DATABASE_NAME")
)

engine = create_engine(url_object)

app = FastAPI()

create_routes(app, engine)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()

@app.get("/hello")
async def read_root():
    return {"Hello, World !"}

@app.get("/exit")
async def hello():
    subprocess.call(["pkill", "uvicorn"])
    return {"message": "Server Stopped"}

@app.post("/user/create", response_model=tuple)
async def Create(user: UserCreate):
    if user.password != user.password_repeat:
        return {
            "message" : "Les mots de passe ne correspondent pas"
        }
    query = text("INSERT INTO users (Email, Password, Firstname, Lastname, BirthdayDate, Adress, PostalCode, Age, Meta, Token, Role) VALUES (:email, :password, :firstname, :lastname, :birthday_date, :adress, :postal_code, :age, :meta, :token, :role) RETURNING *")
    salted = user.password + salt
    values = {
        "email" : user.email,
        "password" : str(md5(salted.encode('utf-8')).digest()),
        "firstname" : user.firstname,
        "lastname" : user.lastname,
        "birthday_date" : user.birthday_date,
        "adress" : user.adress,
        "postal_code" : user.postal_code,
        "age" : datetime.now() - user.birthday_date,
        "meta" : "{}",
        "token" : hash_djb2(user.email + user.firstname + user.lastname + salt),
        "role" : "user",

    }
    with engine.begin() as comm:
        try :
            result = comm.execute(query, values)
        except exc.IntegrityError:
            raise mail_exception
        return result.fetchone()
    
@app.post("/connect")
async def connect(infos : UserConnect):
    query = text("SELECT Email, Firstname, Lastname, Role, Token FROM users WHERE Email = :email AND Password = :password;")
    salted = infos.password + salt
    values = {
        "email" : infos.email,
        "password" : str(md5(salted.encode('utf-8')).digest())
    }
    with engine.begin() as comm:
        result = comm.execute(query, values)
        user = result.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect mail or password", headers={"WWW-Authenticate": "Bearer"})
        JWT = jwt.encode({
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            "Email": user.email,
            "Firstname": user.firstname,
            "Lastname": user.lastname,
            "Role" : user.role,
            "token": user.token
            }, SECRET_KEY, algorithm="HS256")
        return {"auth_token": JWT, "token_type": "bearer"}

@app.get("/user/{user_id}", response_model=getUser)
async def GetUser(JWT: Annotated[str, Depends(oauth2_scheme)], user_id: int):
    try:
        authenticatedUser = Authorize(JWT)
    except HTTPException:
        raise credentials_exception
    if authenticatedUser.role == 'admin' :
        query = text("SELECT * FROM usersAdminView WHERE id = :user_id")
    else:
        query = text("SELECT * FROM usersView WHERE id = :user_id")
    values = {
        "user_id" : user_id
    }
    with engine.begin() as comm:
        result = comm.execute(query, values)
        user = result.fetchone()
    if not user:
        raise user_exception
    return user

@app.post("/user/update", response_model=updateUser)
async def UpdateUser(JWT: Annotated[str, Depends(oauth2_scheme)], update : dict):
    try:
        authenticatedUser = Authorize(JWT)
    except HTTPException:
        raise credentials_exception
    user_id = authenticatedUser.id
    select = text("SELECT * FROM usersAdminView WHERE id = :user_id")
    if update.get("id"):
        try:
            uid = int(update.get("id"))
        except ValueError:
            raise id_exception
        if authenticatedUser.role != 'admin' and update.get("id") != authenticatedUser.id:
            HTTPException(
                status_code=403,
                detail=f"Unauthorized to update this user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = update.get("id")
    select_values = {
        "user_id" : user_id
    }
    with engine.begin() as comm:
        try :
           select_result = comm.execute(select, select_values).mappings().one()
        except exc.NoResultFound:
            raise user_exception
    update.update(select_result, **update)
    if authenticatedUser.role == "admin":
        query = text("UPDATE users SET Email = :email, Firstname = :firstname, Lastname = :lastname, BirthdayDate = :birthdaydate, Age = :age, Adress = :adress, Role = :role WHERE id = :user_id RETURNING *")
    else:
        query = text("UPDATE users SET Email = :email, BirthdayDate = :birthdaydate, Adress = :adress WHERE id = :user_id RETURNING *")
    age : date = date.today().year - update.get("birthdaydate").year
    values = {
        "email" : update.get("email"),
        "firstname" : update.get("firstname"),
        "lastname" : update.get("lastname"),
        "birthdaydate" : update.get("birthdaydate"),
        "adress" : update.get("address"),
        "age" : age,
        "role" : update.get("role"),
        "user_id" : user_id
    }
    with engine.begin() as comm:
        try :
            result = comm.execute(query, values)
        except exc.IntegrityError:
            raise mail_exception
        response = result.fetchone()
        return response