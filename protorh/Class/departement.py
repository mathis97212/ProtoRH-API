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

# Création d'une classe de modèle de base SQLAlchemy.
Base = declarative_base()

# Définition de la classe "Department" qui correspond à la table "Department" dans la base de données.
class Department(Base):
    __tablename__ = "Department"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Définition des classes Pydantic pour gérer les opérations avec les départements.
class AddUserToDepartment(BaseModel):
    __tablename__ = "AddUserToDepartment"
    id: int
    name: str

class RemoveUserFromDepartment(BaseModel):
    __tablename__ = "RemoveUserFromDepartment"
    id: int
    name: str

class GetUsersInDepartment(BaseModel):
    __tablename__ = "GetUsersInDepartment"
    id: int
    name: str
