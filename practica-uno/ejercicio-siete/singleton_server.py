from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import random

class JuegoSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.resultados = []
        return cls._instance

    def jugar(self, elemento_jugador):
        elementos = ["piedra", "papel", "tijera"]
        elemento_servidor = random.choice(elementos)
        resultado = self.calcular_resultado(elemento_jugador, elemento_servidor)
        partida = {
            "id": len(self.resultados) + 1,
            "elemento": elemento_jugador,
            "elemento_servidor": elemento_servidor,
            "resultado": resultado
        }
        self.resultados.append(partida)
        return partida

    def calcular_resultado(self, elemento_jugador, elemento_servidor):
        if elemento_jugador == elemento_servidor:
            return "empató"
        elif (elemento_jugador == "piedra" and elemento_servidor == "tijera") or \
             (elemento_jugador == "tijera" and elemento_servidor == "papel") or \
             (elemento_jugador == "papel" and elemento_servidor == "piedra"):
            return "ganó"
        else:
            return "perdió"

class Partida:
    def __init__(self, elemento_jugador):
        self.juego = JuegoSingleton()
        self.partida = self.juego.jugar(elemento_jugador)

    def to_dict(self):
        return self.partida

class Partidas:
    def __init__(self):
        self.juego = JuegoSingleton()

    def listar_todas(self):
        return self.juego.resultados

    def listar_por_resultado(self, resultado):
        return [partida for partida in self.juego.resultados if partida["resultado"] == resultado]

class PartidaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/partidas":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            partidas = Partidas()
            player_data = json.dumps(partidas.listar_todas())
            self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/partidas":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            elemento = json.loads(post_data.decode("utf-8"))["elemento"]
            partida_nueva = Partida(elemento)
            self.send_response(201)
            self.end_headers()
            player_data = json.dumps(partida_nueva.to_dict())
            self.wfile.write(player_data.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, PartidaHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()
