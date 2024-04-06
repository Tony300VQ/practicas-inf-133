from zeep import Client

client = Client('http://localhost:8000')
result1= client.service.SumaDosNumeros(num1=2,num2=3)
result2= client.service.RestaDosNumeros(num1=10,num2=1)
result3= client.service.MultiplicacionDosNumeros(num1=3,num2=3)
result4= client.service.DivisionDosNumeros(num1=100,num2=0)
print(result1)
print(result2)
print(result3)
print(result4)