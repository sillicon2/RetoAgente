import socket
import sys
#importaciones necesarias
import platform,re,uuid,json,psutil,logging, pprint

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Ip = "127.0.0.1"
puerto = 1244
# Bind the socket to Sthe port
server_address = (Ip, puerto)
print('Agente iniciado en {} en el puerto {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

#funcion que extrae la informacion del sistema
def getSystemInfo():
    #procesos actualmente corriendo
    procesos = []
    for proc in psutil.process_iter():
        try:
            p = proc.name()
            id = proc.pid
            procesos.append([p, id])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    #informacion relevante del sistema
    try:
        info={}
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.system()
        info['processor'] = platform.processor()
        info['users']= psutil.users()
        info['procesos'] = procesos
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)

while True:
    # Wait for a connection
    print('Agente en modo de espera')
    connection, client_address = sock.accept()
    try:
        print('conexion desde: ', client_address)

        # Recibe instrucciones y envia informacion
        while True:
            data = connection.recv(1024)
            #print('Opcion recibida {!r}'.format(data))
            if data:
                if data==b'1':
                    print("enviando informacion")
                    data = getSystemInfo()
                    connection.sendall(bytes(data,encoding="utf-8"))
                    print("informacion enviada")

                    break
                if data==b'2':
                    mensaje2=b'Su Opcion es Salir'
                    connection.sendall(mensaje2)
                    break
            else:
                print('No hay datos del cliente', client_address)
                break
    finally:
        # Clean up the connection
        connection.close()




