# Importation des modules SQLAlchemy nécessaires pour la gestion de la base de données.
from sqlalchemy import create_engine  # Pour créer un moteur de base de données.
from sqlalchemy.orm import sessionmaker  # Pour créer des sessions de base de données.
from sqlalchemy.ext.declarative import declarative_base  # Pour créer une classe de base pour les classes de modèle.
from sqlalchemy_utils import database_exists, create_database  # Pgestion de la database.

# Création de l'URL de la database.
url_object = "postgresql://app:123@localhost/protorh"

# Création d'un moteur SQLAlchemy pour interagir avec la database.
engine = create_engine(url_object)

# Création de la database si elle est pas encore crée.
if not database_exists(engine.url):
    create_database(engine.url, template="template0")

# Configuration d'une session SQLAlchemy afin d'interagir avec la database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création d'une classe de modèle de base SQLAlchemy.
Base = declarative_base()

# Fonction utilitaire pour obtenir une instance du moteur de base de données.
def get_db():
    return engine
     #La session locale est normalement utilisée, mais elle n'est pas correctement gérée dans ce code.
    db = SessionLocal()
    try:
         return db
    finally:
         db.close()

# Création de toutes les tables de # en utilisant la méta-donnée de Base.
Base.metadata.create_all(bind=engine)
