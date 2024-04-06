from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler
dispatcher = SoapDispatcher(
    "ejercicio1.soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)
def sumaDosNumeros(num1,num2):
    return "La suma es: {}".format(num1+num2)
def restaDosNumeros(num1,num2):
    return "La resta es: {}".format(num1-num2)
def multiplicacionDosNumeros(num1,num2):
    return "La multiplicacion es: {}".format(num1*num2)
def divisionDosNumeros(num1,num2):
    if num2!=0:
        return "La division es: {}".format(num1/num2)
    return "No se puede dividir entre 0"

dispatcher.register_function(
    "SumaDosNumeros",
    sumaDosNumeros,
    returns={"suma":str},
    args={"num1":int,"num2":int}
)
dispatcher.register_function(
    "RestaDosNumeros",
    restaDosNumeros,
    returns={"resta":str},
    args={"num1":int,"num2":int}
)
dispatcher.register_function(
    "MultiplicacionDosNumeros",
    multiplicacionDosNumeros,
    returns={"multiplicacion":str},
    args={"num1":int,"num2":int}
)
dispatcher.register_function(
    "DivisionDosNumeros",
    divisionDosNumeros,
    returns={"division":str},
    args={"num1":int,"num2":int}
)

server=HTTPServer(("0.0.0.0",8000), SOAPHandler)
server.dispatcher=dispatcher
print("Servidor iniciado http://localhost:8000/")
server.serve_forever()
