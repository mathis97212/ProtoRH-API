from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

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