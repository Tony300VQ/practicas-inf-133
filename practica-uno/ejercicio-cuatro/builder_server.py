from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
# Base de datos simulada de pizzas
pacientes = {}


# Producto: Pizza
class Paciente:
    def __init__(self):
        self.ci=None
        self.nombre=None
        self.apellido=None
        self.genero=None
        self.edad=None
        self.diagnostico=None
        self.doctor=None

    def __str__(self):
        return f"CI: {self.ci},Nombre: {self.nombre}, Apellido: {self.apellido},Genero: {self.genero}, Edad: {self.edad}, Diagnostico: {self.diagnostico}, Doctor: {self.doctor} "


# Builder: Constructor de pizzas
class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()
    def set_ci(self,ci):
        self.paciente.ci=ci
    def set_nombre(self,nombre):
        self.paciente.nombre=nombre
    def set_apellido(self, apellido):
        self.paciente.apellido=apellido
    def set_genero(self, genero):
        self.paciente.genero= genero
    def set_edad(self,edad):
        self.paciente.edad=edad
    def set_diagnostico(self,diagnostico):
        self.paciente.diagnostico=diagnostico
    def set_doctor(self,doctor):
        self.paciente.doctor=doctor
    def get_paciente(self):
        return self.paciente

# Director: Pizzería
class Hospital:
    def __init__(self, builder):
        self.builder = builder

    def create_paciente(self,ci,nombre,apellido,genero,edad,diagnostico,doctor):
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_genero(genero)
        self.builder.set_edad(edad)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        return self.builder.get_paciente()


# Aplicando el principio de responsabilidad única (S de SOLID)
class HospitalService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)

    def create_paciente(self, post_data):
        ci=post_data.get("ci",None)
        nombre=post_data.get("nombre",None)
        apellido=post_data.get("apellido",None)
        genero=post_data.get("genero",None)
        edad=post_data.get("edad",None)
        diagnostico=post_data.get("diagnostico",None)
        doctor=post_data.get("doctor",None)
        paciente=self.hospital.create_paciente(ci,nombre,apellido,genero,edad,diagnostico,doctor)
        pacientes[len(pacientes)+1]=paciente
        #pizzas[len(pizzas) + 1] = pizza
        
        return paciente

    def read_pacientes(self):
        return {index: patient.__dict__ for index, patient in pacientes.items()}
    def read_pacientes_diagnostico(self,diagnostico):
        return {index: patient.__dict__ for index, patient in pacientes.items() if patient.diagnostico==diagnostico}
    def read_pacientes_doctor(self,doctor):
        return {index: patient.__dict__ for index, patient in pacientes.items() if patient.doctor==doctor}
    def read_pacientes_ci(self,ci):
        return {index: patient.__dict__ for index, patient in pacientes.items() if patient.ci==ci}
    def update_paciente(self, index, data):
        if index in pacientes:
            paciente = pacientes[index]
            ci=data.get("ci",None)
            nombre=data.get("nombre",None)
            apellido=data.get("apellido",None)
            genero=data.get("genero",None)
            edad=data.get("edad",None)
            diagnostico=data.get("diagnostico",None)
            doctor=data.get("doctor",None)
            if ci:
                paciente.ci = ci
            if nombre:
                paciente.nombre=nombre
            if apellido:
                paciente.apellido=apellido
            if genero:
                paciente.genero=genero
            if edad:
                paciente.edad=edad
            if diagnostico:
                paciente.diagnostico=diagnostico
            if doctor:
                paciente.doctor = doctor
            return paciente
        else:
            return None

    def delete_paciente(self, index):
        if index in pacientes:
            return pacientes.pop(index)
        else:
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


# Manejador de solicitudes HTTP
class HospitalHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = HospitalService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/pacientes":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = self.controller.read_pacientes_diagnostico(diagnostico)
                if pacientes_filtrados != []:
                    HTTPDataHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = self.controller.read_pacientes_doctor(doctor)
                if pacientes_filtrados != []:
                    HTTPDataHandler.handle_response(self, 200, pacientes_filtrados)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
            else:
                response_data=self.controller.read_pacientes()
                HTTPDataHandler.handle_response(self, 200, response_data)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = self.controller.read_pacientes_ci(ci)
            if paciente:
                HTTPDataHandler.handle_response(self, 200, paciente)
            else:
                HTTPDataHandler.handle_response(self, 204, [])
        else:
            HTTPDataHandler.handle_response(self, 204, {"Error":"Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(index,data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de pizza no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            deleted_paciente = self.controller.delete_paciente(index)
            if deleted_paciente:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Paciente eliminada correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=HospitalHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
