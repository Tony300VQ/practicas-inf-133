import requests

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}


response = requests.get(url)
print(response.json())

patient_update={
        "ci":109027,
        "nombre": "Pedrito",
        "apellido": "García",
        "edad": 21,
        "genero":"Male",
        "diagnostico":"Good",
        "doctor":"Pedro Pérez"}
response = requests.post(url, json=patient_update, headers=headers)
print(response.json())

response = requests.get(url)
print(response.json())


patient_update2={
        "ci":109027,
        "nombre": "Pedrito",
        "apellido": "García",
        "edad": 23,
        "genero":"Male",
        "diagnostico":"Good",
        "doctor":"Pedro Pérez"}
response = requests.put(url+"/1", json=patient_update2, headers=headers)
print(response.json())
print("////")

response = requests.get(url)
print(response.json())



response = requests.delete(url + "/1")
print(response.json())

response = requests.get(url)
print(response.json())