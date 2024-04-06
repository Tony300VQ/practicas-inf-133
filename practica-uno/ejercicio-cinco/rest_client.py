import requests

# Consultando a un servidor RESTful
url = "http://localhost:8000/"

ruta_get = url + "animales"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_post = url + "animales"
new_animal = {
        "id": 2,
        "nombre": "Leon",
        "especie": "Panthera leo",
        "genero":"Femenino",
        "edad":10,
        "peso":50.4
}
post_response = requests.request(method="POST", url=ruta_post, json= new_animal)
print(post_response.text)



ruta_get = url + "animales?especie=Panthera leo"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#
ruta_get = url + "animales?genero=Masculino"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
#
animal2 = {
        "id": 2,
        "nombre": "Leon",
        "especie": "Panthera leo",
        "genero":"Female",
        "edad":20,
        "peso":60.3
}
ruta_put = url+"animales/2"
put_response= requests.request(method="PUT",url=ruta_put,json=animal2)
print(put_response.text)
ruta_delete = url+"animales/1"
delete_response = requests.request(method="DELETE",url=ruta_delete)
print(delete_response.text)
