import subprocess, uvicorn
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Float, text, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from pydantic import BaseModel

DATABASE_URL = "postgresql://jawa:123@localhost/ProtoRH"

create = create_engine(DATABASE_URL)
if not database_exists(engine.url):
    create_database(engine.url, template="template0")

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
base = declarative_base

app = FastAPI()

# Endpoint : /
# Type : GET
# this endpoint return à json string containing "Hello world !"
@app.get("/")
async def read_root():
    return {"Hello world !"}

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import jwt
import datetime

app = FastAPI()

# Clé secrète pour JWT (à remplacer par votre clé réelle)
SECRET_KEY = 'votre_clé_secrète_jwt'

# Base de données (simulation)
demandes_rh = []

# Modèles Pydantic pour les données
class DemandeRH(BaseModel):
    id_user: int
    content: str

# Middleware pour vérifier le JWT
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return 'Jetons JWT expiré'
    except jwt.InvalidTokenError:
        return 'Jetons JWT non valides'

# Endpoint création  d'une demande RH
@app.post('/rh/msg/add')
def add_demande_rh(demande: DemandeRH, request: Request):
    token = request.headers.get('Authorization')
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Accès refusé')

    current_date = datetime.datetime.now()

    nouvelle_demande = {
        'registration_date': current_date.isoformat(),
        'visibility': True,
        'close': False,
        'last_action': current_date.isoformat(),
        'content': [
            {
                'author': demande.id_user,
                'content': demande.content,
                'date': current_date.isoformat()
            }
        ]
    }

    demandes_rh.append(nouvelle_demande)

    return nouvelle_demande
# Endpoint demande RH non visible
@app.post('/rh/msg/remove')
def remove_demande_rh(message_id: int, request: Request):
    token = request.headers.get('Authorization')
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Accès refusé')

    for demande_rh in demandes_rh:
        if demande_rh['content'][0]['author'] == payload['user_id']:
            # La demande est considérée  comme non visible
            demande_rh['visibility'] = False
            # Maj last_action et delete_date
            current_date = datetime.datetime.now()
            demande_rh['last_action'] = current_date.isoformat()
            demande_rh['delete_date'] = current_date.isoformat()

    return 'Demande marquée comme non visible'

# Endpoint maj une demande RH
@app.post('/rh/msg/update')
def update_demande_rh(demande: DemandeRH, request: Request):
    token = request.headers.get('Authorization')
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Accès refusé')

    current_date = datetime.datetime.now()

    for demande_rh in demandes_rh:
        if demande_rh['content'][0]['author'] == demande.id_user:
            demande_rh['last_action'] = current_date.isoformat()
            new_content = {
                'author': demande.id_user,
                'content': demande.content,
                'date': current_date.isoformat()
            }
            demande_rh['content'].append(new_content)

    return 'Demande mise à jour avec succès'

# Endpoint pour récupérer les demandes RH
@app.get('/rh/msg')
def get_demandes_rh(request: Request):
    token = request.headers.get('Authorization')
    payload = verify_jwt(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Accès refusé')

    if payload['role'] not in ['manager', 'admin']:
        raise HTTPException(status_code=403, detail='Accès refusé : seuls les managers et les administrateurs peuvent voir les demandes')

    # jointure avec les utilisateurs si nécessaire
    # renvoi simplement les demandes RH existantes
    return demandes_rh