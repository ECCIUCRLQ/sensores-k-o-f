import socket
import struct

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for i in range(0,100):
        string_send = bytearray("Hello, world", 'utf-8')
		# string_send = b'Hello, world'
        package_format = "B" + str(len(string_send)) + "s"
        package = struct.pack(package_format, 0, string_send)
        s.sendall(package)
        data = s.recv(192706)
        
    s.shutdown(1)
    s.close()

print('Received', repr(data))