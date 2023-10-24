import subprocess, uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

DATABASE_URL = "postgresql://jawa:123@localhost/ProtoRH"

app = FastAPI()

# Endpoint : /
# Type : GET
# this endpoint return à json string containing "Hello world !"
@app.get("/")
async def read_root():
    return {"Hello world !"}