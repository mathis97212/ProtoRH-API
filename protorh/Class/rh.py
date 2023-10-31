from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# Exemple de stockage des demandes RH en mémoire (remplacez par une base de données réelle).
requests_data = []

class RequestItem(BaseModel):
    id_user: int
    content: str

class RequestResponse(BaseModel):
    message: str

class RequestDetail(BaseModel):
    id: int
    id_user: int
    content: str
    registration_date: datetime
    visibility: bool
    close: bool
    last_action: datetime
    content_history: List[dict]

@app.post('/rh/msg/add', response_model=RequestResponse)
def add_request(request: RequestItem):
    request_data = {
        'id': len(requests_data) + 1,
        'id_user': request.id_user,
        'content': request.content,
        'registration_date': datetime.now(),
        'visibility': True,
        'close': False,
        'last_action': datetime.now(),
        'content_history': []
    }
    requests_data.append(request_data)
    return {'message': 'Demande RH ajoutée avec succès!'}

@app.post('/rh/msg/remove', response_model=RequestResponse)
def remove_request(request_id: int):
    for request_data in requests_data:
        if request_data['id'] == request_id:
            request_data['visibility'] = False
            request_data['close'] = True
            request_data['last_action'] = datetime.now()
            return {'message': 'Demande RH rendue non visible!'}
    raise HTTPException(status_code=404, detail='Demande RH non trouvée')

@app.post('/rh/msg/update', response_model=RequestResponse)
def update_request(request_id: int, request: RequestItem):
    for request_data in requests_data:
        if request_data['id'] == request_id:
            request_data['last_action'] = datetime.now()
            request_data['content_history'].append({
                'author': request.id_user,
                'content': request.content,
                'date': datetime.now()
            })
            return {'message': 'Demande RH mise à jour avec succès!'}
    raise HTTPException(status_code=404, detail='Demande RH non trouvée')

@app.get('/rh/msg', response_model=List[RequestDetail])
def get_requests():
    # Vous devrez implémenter la vérification des droits de l'utilisateur ici.
    # Vous pouvez également implémenter une jointure avec d'autres données si nécessaire.
    visible_requests = [request_data for request_data in requests_data if request_data['visibility']]
    return visible_requests
