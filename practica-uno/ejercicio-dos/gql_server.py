from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, Boolean, List, Schema, Field, Mutation


class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad= String()
    altura = String()
    frutos= Boolean()

class Query(ObjectType):
    plantas = List(Planta)
    planta_por_id = Field(Planta, id=Int())
    plantas_por_especie = List(Planta, especie=String())
    plantas_poseen_frutos = List(Planta)
    def resolve_plantas(root, info):
        return plantas
    
    def resolve_planta_por_id(root, info, id):
        for planta in plantas:
            if planta.id == id:
                return planta
        return None
    def resolve_plantas_por_especie(root,info,especie):
        plantas2=[]
        for planta in plantas:
            if planta.especie == especie:
                plantas2.append(planta)
        return plantas2
    def resolve_plantas_poseen_frutos(root,info):
        plantas2=[]
        for planta in plantas:
            if planta.frutos==True:
                plantas2.append(planta)
        return plantas2
class CrearPlanta(Mutation):
    class Arguments:
        nombre=String()
        especie = String()
        edad = String()
        altura = String()
        frutos = Boolean()

    planta = Field(Planta)

    def mutate(root, info, nombre,especie,edad,altura,frutos):
        nueva_planta = Planta(
            id=len(plantas) + 1, 
            nombre=nombre, 
            especie=especie, 
            edad=edad,
            altura=altura,
            frutos=frutos
        )
        plantas.append(nueva_planta)
        return CrearPlanta(planta=nueva_planta)
class UpDatePlanta(Mutation):
    class Arguments:
        id=Int()
        nombre=String()
        especie=String()
        edad=String()
        altura=String()
        frutos =Boolean()
    planta=Field(Planta)
    def mutate(root,info,id,nombre,especie,edad,altura,frutos):
        for i,planta in enumerate(plantas):
            if planta.id==id:
                plantas[i]=Planta(id=id,nombre=nombre,especie=especie,edad=edad,altura=altura,frutos=frutos)
                return UpDatePlanta(planta=plantas[i])
        return None
class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None

class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    up_date_planta = UpDatePlanta.Field()

plantas = [
    Planta(
        id=1, nombre="Tomate", especie="Solanum lycopersicum", edad = "1 mes", altura="2 cm", frutos=True
    ),
    Planta(id=2, nombre="Lechuga", especie="Lactuca sativa", edad="3 meses", altura="10 cm", frutos=False),
]

schema = Schema(query=Query, mutation=Mutations)


class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
