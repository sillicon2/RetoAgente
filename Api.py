import socket, pprint, json, datetime
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ip = "127.0.0.1"
puerto = 1241
today = datetime.date.today()


# Connect the socket to the port where the server is listening
server_address = (Ip, puerto)
print('Conexion con el agente: {} puerto {}'.format(*server_address))
print('************************************')
print('Opciones: ')
print('1. Obtener informacion del agente')
print('2. Salir')
opcion = input('Por favor elija una opcion: ').encode()
sock.connect(server_address)

try:
    # Send data
    #message = b'Conexion con el Agente.  Solicitud de informacion'
    #print('sending {!r}'.format(message))
    sock.sendall(opcion)

    # Look for the response
    amount_received = 0
    while True:
        data = sock.recv(65507) #tamaño maximo a la espera de cantidades de informacion variable
        data = data.decode("utf-8")
        amount_received += len(data)
        print("cantidad de informacion: ", len(data))
        print('Mensaje Agente:  {!r}'.format(data))
        break
finally:
    print('closing socket')
    sock.close()

dataParsing = json.loads(data)
nombreArchivo = str(Ip) + '_'+ str(today) + ".json"
with open(nombreArchivo, 'w') as file:
    json.dump(dataParsing, file)

print("los datos fueron guardados en como: ",nombreArchivo)

