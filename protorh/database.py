import subprocess, uvicorn
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, text, JSON, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

url_object2 = URL.create(
    "postgresql",
    username=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    database=os.getenv("DATABASE_NAME") 
)

url_object = "postgresql://app:123@localhost/protorh"

engine = create_engine(url_object)
if not database_exists(engine.url):
    create_database(engine.url, template="template0")
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    return engine
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
Base.metadata.create_all(bind=engine)
