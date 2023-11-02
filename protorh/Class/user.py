# Importation des modules et bibliothèques nécessaires.
from sqlalchemy import create_engine, Column, Integer, Float, String, text, Date, JSON, Boolean  # Pour la gestion de la base de données.
from sqlalchemy.ext.declarative import declarative_base  # Pour créer une classe de base pour les classes de modèle.
from pydantic import BaseModel, Json  # Pour définir des modèles Pydantic.
from datetime import date  # Pour travailler avec les dates.

# Création d'une classe de modèle de base SQLAlchemy.
Base = declarative_base()

# Définition de la classe "User" qui correspond à la table "users" dans la base de données.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    password_repeat = Column(String, index=True)
    lastname = Column(String, index=True)
    firstname = Column(String, index=True)
    birthdaydate = Column(String, index=True)
    address = Column(String, index=True)
    postalcode = Column(String, index=True)
    age = Column(Integer)
    meta = Column(JSON)
    registrationdate = Column(String)
    token = Column(String, index=True)
    role = Column(String, index=True)
    departements = Column(Integer, nullable=True)

# Définition des classes Pydantic pour gérer les opérations liées aux utilisateurs.
class Create(BaseModel):
    email: str
    password: str
    password_repeat: str
    firstname: str
    lastname: str
    birthdaydate: date
    address: str
    postalcode: str

class Update(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    birthdaydate: date
    address: str
    postalcode: str
    age: int

class UpdatePassword(BaseModel):
    email: str
    password: str

class UserConnect(BaseModel):
    email: str
    password: str

class GetUser(BaseModel):
    id: int
    email: str
    password: str
    firstname: str
    lastname: str
    birthdaydate: date
    address: str
    postalcode: str
    age: int
    meta: str
    registrationdate: date
    token: str
    role: str
    departements: int

class UploadProfilePicture(BaseModel):
    email: str
    password: str
    firstname: str
    lastname: str
    birthdaydate: date
    address: str
    postalcode: str
    age: int
