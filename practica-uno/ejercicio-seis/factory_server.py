from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

# Base de datos simulada de vehículos
animales = {}


class Animal:
    def __init__(self, animal_type, nombre, especie, genero, edad, peso):
        self.animal_type = animal_type
        self.nombre= nombre
        self.especie = especie
        self.genero = genero
        self.edad = edad
        self.peso = peso

class Mamifero(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("mamifero", nombre, especie, genero, edad, peso)
class Ave(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("ave", nombre, especie, genero, edad, peso)
class Reptil(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("reptil",nombre, especie, genero, edad, peso)
class Anfibio(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("anfibio", nombre, especie, genero, edad, peso)
class Pez(Animal):
    def __init__(self, nombre, especie, genero, edad, peso):
        super().__init__("pez", nombre, especie, genero, edad, peso)


class AnimalFactory:
    @staticmethod
    def create_animal(animal_type, nombre,especie, genero, edad, peso):
        if animal_type == "mamifero":
            return Mamifero(nombre,especie,genero, edad, peso)
        elif animal_type == "ave":
            return Ave(nombre,especie,genero, edad, peso)
        elif animal_type == "reptil":
            return Reptil(nombre,especie,genero, edad, peso)
        elif animal_type == "anfibio":
            return Anfibio(nombre,especie,genero, edad, peso)
        elif animal_type == "pez":
            return Pez(nombre,especie,genero, edad, peso)
        else:
            raise ValueError("Tipo de animal no válido")


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


class ZooService:
    def __init__(self):
        self.factory = AnimalFactory()

    def add_animal(self, data):
        animal_type = data.get("animal_type", None)
        nombre = data.get("nombre",None)
        especie = data.get("especie",None)
        genero = data.get("genero",None)
        edad = data.get("edad",None)
        peso = data.get("peso", None)
        
        animal = self.factory.create_animal(
            animal_type, nombre,especie,genero,edad,peso
        )
        animales[len(animales) + 1] = animal
        return animal

    def list_animals(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    def list_animals_by_especie(self,species):
        return {index: animal.__dict__ for index, animal in animales.items() if animal.especie==species}
    def list_animals_by_genero(self,genero):
        return {index: animal.__dict__ for index, animal in animales.items() if animal.genero==genero}
    def list_animals_by_id(self,id):
        return {index: animal.__dict__ for index, animal in animales.items() if index==id}
    
    def update_animal(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            especie = data.get("especie", None)
            genero = data.get("genero", None)
            peso = data.get("peso", None)
            if nombre:
                animal.nombre=nombre
            if especie:
                animal.especie=especie
            if genero:
                animal.genero=genero
            if peso:
                animal.peso=peso
            return animal
        else:
            raise None

    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "Animal eliminado"}
        else:
            return None


class ZooRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoo_service = ZooService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoo_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = self.zoo_service.list_animals_by_especie(especie)
                if animales_filtrados != []:
                    HTTPDataHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = self.zoo_service.list_animals_by_genero(genero)
                if animales_filtrados != []:
                    HTTPDataHandler.handle_response(self, 200, animales_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            else:
                response_data=self.zoo_service.list_animals()
                HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/animales/"):
            id = int(self.path.split("/")[-1])
            animal = self.zoo_service.list_animals_by_id(id)
            if animal:
                HTTPDataHandler.handle_response(self, 200, animal)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        else:
            HTTPDataHandler.handle_response(self, 204, {"Error":"Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoo_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoo_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZooRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()