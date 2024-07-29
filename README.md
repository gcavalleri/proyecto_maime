# proyecto_maime
trabajo final para introduccion al software


#PUT
curl -X PUT http://127.0.0.1:5000/cartas/1 -H "Content-Type: application/json" -d '{"nombre": "Carta Actualizada", "imagen": "nueva-ruta-carta"}'

#DELETE
curl -X DELETE http://127.0.0.1:5000/cartas/{id-de-carta}

#POST
curl -X POST http://127.0.0.1:5000/cartas -H "Content-Type: application/json" -d '{"nombre": "Carta Nueva", "imagen": "{ruta-carta}"}'

#GET
curl -X GET http://127.0.0.1:5000/cartas
