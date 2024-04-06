import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'



query_crear = """
mutation {
        crearPlanta(nombre: "Tomate", especie: "Solanum lycopersicum",edad: "2 meses", altura: "15 cm",frutos: true) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""

response = requests.post(url, json={'query': query_lista})
print(response.text)

query1 = """
    {
        plantasPorEspecie(especie: "Solanum lycopersicum"){
            nombre
            edad
            altura
            frutos
        }
    }
"""


response = requests.post(url, json={'query': query1})
print(response.text)
query2 = """
    {
        plantasPoseenFrutos{
            nombre
            especie
            edad
            altura
        }
    }
"""


response = requests.post(url, json={'query': query2})
print(response.text)


query0 = """
mutation
{
    upDatePlanta(id:1,nombre:"n1",especie:"Solanum lycopersicum",edad:"2 meses",altura:"12.4 cm",frutos: false)
    {
        planta
        {
            id
            nombre
            especie
        }
    }
}
"""
response= requests.post(url, json={"query": query0})
print(response.text)

query_eliminar = """
mutation {
        deletePlanta(id: 2) {
            planta {
                id
                nombre
                especie
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

# Lista de todos las plantas
response = requests.post(url, json={'query': query_lista})
print(response.text)