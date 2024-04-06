import requests

url = "http://localhost:8000/"

ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_post = url + "mensajes"
nuevo_mensaje = {
    "contenido": "Hola",
}
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_mensaje)
print(post_response.text)

ruta_put = url+"mensajes/2"
mensaje_actualizado={
    "contenido":"Hola mundo"
}
put_response= requests.request(method="PUT",url=ruta_put, json=mensaje_actualizado)
print(put_response.text)
ruta_get = url + "mensajes/1"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

ruta_delete = url + "mensajes/1"
delete_response = requests.request(method="DELETE", url = ruta_delete)
print(delete_response.text)