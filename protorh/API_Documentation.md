# Documentation des Endpoints

## Endpoint : / (GET)

- L'endpoint `/` renvoie une chaîne JSON contenant "Hello world !".

### Informations Requises

Aucune information requise.

### Exemple de Retour Possible

```json
{
  "message": "Hello world !"
}
```

## Exemple de Requête Curl:

curl -X GET "http://localhost:4243/"

## Description des Cas d'Utilisation

Cet endpoint est utilisé pour vérifier que l'API est en ligne.


## Endpoint : /user/create (POST)

- L'endpoint /user/create crée un utilisateur.

### Informations Requises

les informations de l'utilisateur à créer, y compris email, firstname, lastname, password, password_repeat, postalcode, et d'autres champs.

### Exemple de Retour Possible

```json
{
  "message": "User created"
}
```

## Exemple de Requête Curl:

curl -X POST "http://localhost:4243/user/create/" -d '{"email": "mathis@gmail.com", "firstname": "Mathis", "lastname": "Diallo", "password": "123", "password_repeat": "123", "postalcode": "77120"}'

## Description des Cas d'Utilisation

Cet endpoint est utilisé pour créer un nouvel utilisateur en vérifiant les informations fournies, notamment la correspondance des mots de passe et la validité du code postal.


## Endpoint : /connect (POST)

- L'endpoint /connect permet de se connecter en tant qu'utilisateur.

### Informations Requises

les informations de connexion de l'utilisateur, y compris email et password.

### Exemple de Retour Possible

```json
{
  "message": "Successful connection",
  "token": "token"
}
```

## Exemple de Requête Curl:

curl -X POST "http://localhost:4243/connect/" -d '{"email": "mathis@gmail.com", "password": "123"}'

## Description des Cas d'Utilisation

Cet endpoint est utilisé pour permettre aux utilisateurs de se connecter en vérifiant leurs informations de connexion. Un jeton d'accès est renvoyé en cas de succès.


## Endpoint : /user/{id} (GET)

- L'endpoint /user/{id} fournit des informations sur un utilisateur spécifique.

### Informations Requises

L'ID de l'utilisateur pour lequel vous souhaitez obtenir des informations.

### Exemple de Retour Possible

```json
{
  "id": 1,
  "email": "mathis@gmail.com",
  "firstname": "Mathis",
  "lastname": "Diallo",
  "age": 18,
  "role": "user"
}
```

## Exemple de Requête Curl:

curl -X GET "http://localhost:4243/user/1" -H "Authorization: Bearer 2326095998"

## Description des Cas d'Utilisation

Cet endpoint est utilisé pour obtenir des informations détaillées sur un utilisateur spécifique en fonction de son ID. Les informations renvoyées dépendent du rôle de l'utilisateur.


## Endpoint : /user/update (POST)

- L'endpoint /user/update permet de mettre à jour les informations de l'utilisateur.

### Informations Requises

les informations de l'utilisateur à mettre à jour, y compris id, email, firstname, lastname, birthdaydate, address, postalcode, age, meta, registrationdate, role, departements, et d'autres champs en fonction du rôle.

### Exemple de Retour Possible

```json
{
  "message": "Successful update",
  "details": "User information updated successfully"
}
```

## Exemple de Requête Curl:

curl -X POST "http://localhost:4243/user/update -d '{"id": 1, "email": "Ilyes@gmail.com", "firstname": "Ilyes", "lastname": "Bennali", "birthdaydate": "2005-01-01", "address": "123", "postalcode": "77000", "age": 18, "meta": {}, "registrationdate": "2023-01-01", "role": "user", "departements": "None"}'

## Description des Cas d'Utilisation

Cet endpoint est utilisé pour mettre à jour les informations d'un utilisateur en fonction de son ID, en veillant à respecter les règles de mise à jour en fonction du rôle de l'utilisateur.


## Endpoint : /user/password (POST)

- L'endpoint /user/password permet de mettre à jour le mot de passe de l'utilisateur.

### Informations Requises

les informations de l'utilisateur pour mettre à jour le mot de passe, y compris email, password, new_password, et new_password_repeat.

### Exemple de Retour Possible

```json
{
  "message": "Successful update",
  "details": "User password updated successfully"
}
```

## Exemple de Requête Curl:

curl -X POST "http://localhost:4243/user/update -d '{"email": "mathis@gmail.com", "password": "123", "new_password": "newpassword123", "new_password_repeat": "newpassword123"}'

## Description des Cas d'Utilisation

Cet endpoint est utilisé pour mettre à jour le mot de passe de l'utilisateur en vérifiant la correspondance des mots de passe.