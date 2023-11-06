from fastapi import FastAPI
from routes import router
from dotenv import load_dotenv
import os

load_dotenv(".env")

SALT = os.getenv("feur")
SECRET_KEY = os.getenv("feur123")
DATABASE_HOST = os.getenv("localhost")
DATABASE_PORT =os.getenv("4243")
DATABASE_NAME = os.getenv("protorh")
DATABASE_USER = os.getenv("ilyes")
DATABASE_PASSWORD = os.getenv("1234")

app = FastAPI()
app.include_router(router, tags=["routes"])

