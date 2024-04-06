import requests
url = "http://localhost:8000/"
# GET
ruta_get = url+"pacientes"
get_response = requests.request(method="GET", url=ruta_get)
print("////")
print(get_response.text)
print("////")
# POST 
ruta_post = url + "pacientes"
new_patient = {
    "ci":234432,
    "nombre": "Juanito",
    "apellido": "Pérez",
    "edad":23,
    "genero":"Masculino",
    "diagnostico":"Diabetes",
    "doctor":"Pedro Perez"
}
post_response = requests.request(method="POST", url=ruta_post, json=new_patient)
print(post_response.text)

ruta_get = url + "pacientes/234432"
get_response = requests.request(method="GET",url=ruta_get)
print(get_response.text)
# GET with Query pharams
ruta_get = url + "pacientes?diagnostico=Diabetes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
ruta_get = url + "pacientes?doctor=Pedro Perez"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)
patient_update={
        "ci":109027,
        "nombre": "Pedrito",
        "apellido": "García",
        "edad": 21,
        "genero":"Masculino",
        "diagnostico":"Good",
        "doctor":"Pedro Pérez"}
ruta_put = url + "pacientes/109027"
put_response = requests.request(method="PUT", url=ruta_put,json=patient_update)
print(put_response.text)
ruta_get = url + "pacientes/234432"
delete_response = requests.request(method="DELETE", url=ruta_get)
print(delete_response.text)
ruta_get = url + "pacientes"
print("//////")
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)