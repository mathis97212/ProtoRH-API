# Importation des modules et bibliothèques nécessaires.
import subprocess  # Pour lancer des sous-processus (non utilisé dans ce code).
import uvicorn  # Pour exécuter l'application FastAPI avec Uvicorn.
import os  # Pour interagir avec le système d'exploitation.
from sqlalchemy import create_engine, Column, Integer, Float, String, text, Date, JSON, Boolean  # Pour la gestion de la base de données.
from sqlalchemy.orm import sessionmaker  # Pour créer des sessions de base de données.
from sqlalchemy.ext.declarative import declarative_base  # Pour créer une classe de base pour les classes de modèle.
from sqlalchemy_utils import database_exists, create_database  # Pour la gestion de la base de données.
from pydantic import BaseModel  # Pour définir des modèles Pydantic.
from fastapi import FastAPI  # Importation de la classe FastAPI.
from datetime import date  # Pour travailler avec les dates.

# Création d'une classe de modèle de base SQLAlchemy.
Base = declarative_base()

# Définition de la classe "RequestRH" qui correspond à la table "RequestRH" dans la base de données.
class RequestRH(Base):
    __tablename__ = "RequestRH"
    id = Column(Integer, primary_key=True, index=True)
    UserID = Column(Integer)
    Content = Column(String)
    RegistrationDate = Column(Date)
    Visibility = Column(Boolean)
    Close = Column(Boolean)
    LastAction = Column(Boolean)
    ContentHistory = Column(JSON)

# Définition des classes Pydantic pour gérer les opérations liées aux demandes RH.
class CreateRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: date
    Visibility: bool
    Close: bool
    LastAction: bool
    ContentHistory: str

class UpdateRequestRH(BaseModel):
    id: int
    UserID: int
    Content: str
    RegistrationDate: date
    Visibility: str
    Close: str
    LastAction: str
    ContentHistory: str

class RemoveRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: date
    Visibility: str
    Close: str
    LastAction: str
    ContentHistory: str

class GetRequestRH(BaseModel):
    UserID: int
    Content: str
    RegistrationDate: date
    Visibility: str
    Close: str
    LastAction: str
    ContentHistory: str
