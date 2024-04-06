import requests
import json

url = "http://localhost:8000/animales"
headers = {"Content-Type": "application/json"}

# POST /deliveries
new_animal_data = {
        "animal_type":"mamifero",
        "nombre": "Leon",
        "especie": "Panthera leo",
        "genero":"Femenino",
        "edad":10,
        "peso":50.4
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())

new_animal_data = {
        "animal_type":"mamifero",
        "nombre": "Tigre",
        "especie": "Panthera tigher",
        "genero":"Masculino",
        "edad":14,
        "peso":60
}
response = requests.post(url=url, json=new_animal_data, headers=headers)
print(response.json())



response = requests.get(url=url)
print(response.json())


animal_id_to_update = 1
updated_animal_data ={
        "edad":20,
        "peso":60
}
response = requests.put(f"{url}/{animal_id_to_update}", json=updated_animal_data)
print("Animal actualizado:", response.json())

response = requests.get(url=url)
print(response.json())




response = requests.get(url=url)
print(response.json())
response = requests.get(url=url+"?genero=Femenino")
print(response.json())
response = requests.get(url=url+"?especie=Panthera tigher")
print(response.json())
response = requests.get(url=url+"/1")
print(response.json())

animal_id_to_delete = 1
response = requests.delete(f"{url}/{animal_id_to_delete}")
print("Animal eliminado:", response.json())