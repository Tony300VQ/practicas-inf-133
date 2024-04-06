from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

mensajes = [
    {
    "id":1,
    "contenido":"a",
    "contenido_encriptado":"d",
    },
]


class MensajesService:
    @staticmethod
    def find_mensaje(id):
        return next(
            (mensaje for mensaje in mensajes if mensaje["id"] == id),
            None,
        )

    #@staticmethod
    #def filter_students_by_name(nombre):
    #    return [
    #        estudiante for estudiante in estudiantes if estudiante["nombre"] == nombre
    #    ]

    @staticmethod
    def cifrar(texto):
        texto_cifrado = ''
        for caracter in texto:
            if caracter.isalpha():
                if caracter.isupper():
                    inicio = ord('A')
                else:
                    inicio = ord('a')
                indice = (ord(caracter) - inicio + 3) % 27 + inicio
                if indice == 0:
                    indice += 27
                if indice == 32:
                    indice -= 1
                texto_cifrado += chr(indice)
            else:
                texto_cifrado += caracter
        return texto_cifrado
    @staticmethod
    def add_mensaje(data):
        data["id"] = len(mensajes) + 1
        data["contenido_encriptado"] = MensajesService.cifrar(data["contenido"])
        mensajes.append(data)
        return mensajes

    @staticmethod
    def update_mensaje(id, data):
        mensaje = MensajesService.find_mensaje(id)
        if mensaje:
            data["contenido_encriptado"] = MensajesService.cifrar(data["contenido"])
            mensaje.update(data)
            return mensajes
        else:
            return None

    @staticmethod
    def delete_mensaje(id):
        for i, mensaje in enumerate(mensajes):
            if mensaje["id"]==id:
                mensajes.pop(i)
                return mensajes
        return None


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



class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/mensajes":
            HTTPDataHandler.handle_response(self, 200, mensajes)
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = MensajesService.find_mensaje(id)
            if mensaje:
                HTTPDataHandler.handle_response(self, 200, [mensaje])
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )
    def do_POST(self):
        if self.path == "/mensajes":
            data = HTTPDataHandler.handle_reader(self)
            mensajes = MensajesService.add_mensaje(data)
            HTTPDataHandler.handle_response(self, 201, mensajes)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            mensajes = MensajesService.update_mensaje(id,data)
            if mensajes:
                HTTPDataHandler.handle_response(self, 200, mensajes)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Estudiante no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensajes = MensajesService.delete_mensaje(id)
            HTTPDataHandler.handle_response(self, 200, mensajes)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()