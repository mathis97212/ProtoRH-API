# J'importe les classes nécessaires depuis SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

# Je définis l'URL de ma base de données PostgreSQL
# Je remplace 'ilyes', '1234', 'localhost', et 'protorh' par mes propres identifiants, mots de passe et nom de ma base de données
url_object = "postgresql://ilyes:1234@localhost/protorh"

# Je crée un moteur SQLAlchemy en utilisant l'URL de ma base de données
engine = create_engine(url_object)

# Je vérifie si ma base de données existe, sinon je la crée en utilisant le modèle template0
if not database_exists(engine.url):
    create_database(engine.url, template="template0")

# Je crée une session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Je crée une classe de base pour mes modèles SQLAlchemy
Base = declarative_base()

# Fonction pour obtenir l'instance de mon moteur de base de données
def get_db():
    return engine

# Je crée toutes les tables dans ma base de données en utilisant le modèle associé
Base.metadata.create_all(bind=engine)
