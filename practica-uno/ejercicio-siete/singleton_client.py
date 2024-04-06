import requests

url = "http://localhost:8000/"

response = requests.request(method="GET", url=url + "partidas")
print(response.text)

response = requests.request(
    method="POST", url=url + "partidas", json={"elemento": "piedra"}
)
print(response.text)

response = requests.request(method="GET", url=url + "partidas")
print(response.text)