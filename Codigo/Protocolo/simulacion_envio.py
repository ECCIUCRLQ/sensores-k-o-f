import socket
import struct
import time

#HOST = '10.1.137.27'  # The server's hostname or IP address
HOST = '127.0.0.1'
PORT = 2000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    #string_send = bytearray("Esto es un String de prueba" , 'utf-8')
    #string_send = b'Hello, world'
    package_format = "=BBII" 
    #+ str(len(string_send)) + "s"
    package = struct.pack(package_format, 0, 1, 4, 1000)
    #time.sleep(1)
    s.sendall(package)
    data = s.recv(192706)
    print(str(data))
    
    time.sleep(2)
    
    package_format_2 = "=BB"
    package_2 = struct.pack(package_format_2, 1, 1)
    
    s.sendall(package_2)
    print("Mandé paquete lectura")
    data = s.recv(692000)
    print(str(data))
    information = struct.unpack("=I", data[2:6])
    print("La pagina que guarde es: " + str(information[0]))
        
    s.shutdown(1)
    s.close()
