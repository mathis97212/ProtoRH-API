import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel
from routes import router


from Class.departement import Department, AddUserToDepartment, RemoveUserFromDepartment, GetUsersInDepartment
from Class.user import User, Create, Update, UpdatePassword, UploadProfilePicture
from Class.requestrh import RemoveRequestRH, UpdateRequestRH, RequestRH, GetRequestRH
from Class.event import Event, CreateEvent, GetEvent, RemoveEvent

 
app = FastAPI()
app.include_router(router, tags=["routes"])
