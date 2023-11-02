# Importation de la classe FastAPI depuis le module fastapi.
from fastapi import FastAPI
# Importation du router défini dans le module routes.
from routes import router
# Création d'une instance de l'application FastAPI.
app = FastAPI()
# mise en place du routeur (router) dans l'application FastAPI.
# Le routeur contient des endpoints et des itinéraires pour s'occuper des requêtes HTTP.
# Les tags=["routes"] peuvent être utilisés pour organiser les endpoints en différentes catégories.
app.include_router(router, tags=["routes"])