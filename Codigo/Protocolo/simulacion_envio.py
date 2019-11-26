import socket
import struct
import time

HOST = '10.1.137.27'  # The server's hostname or IP address
PORT = 2000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    string_send = bytearray("Esto es un String de prueba" , 'utf-8')
    # string_send = b'Hello, world'
    package_format = "B" + str(len(string_send)) + "s"
    package = struct.pack(package_format, 0, string_send)
    #time.sleep(1)
    s.sendall(package)
    data = s.recv(192706)
        
    s.shutdown(1)
    s.close()

print('Received', repr(data))