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

# Définition de la classe "Event" qui correspond à la table "Event" dans la base de données.
class Event(Base):
    __tablename__ = "Event"
    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, index=True)
    Date = Column(Integer, index=True)
    Description = Column(String, index=True)
    UserID = Column(Integer, index=True)
    DepartmentID = Column(Integer, index=True)

# Définition des classes Pydantic pour gérer les opérations liées aux événements.
class CreateEvent(BaseModel):
    id: int
    Name: str
    Date: date
    Description: str
    UserID: int
    DepartmentID: int

class GetEvent(BaseModel):
    id: int
    Name: str
    Date: date
    Description: str
    UserID: int
    DepartmentID: int

class RemoveEvent(BaseModel):
    id: int
    Name: str
    Date: date
    Description: str
    UserID: int
    DepartmentID: int
