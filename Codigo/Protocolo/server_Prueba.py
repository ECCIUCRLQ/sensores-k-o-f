import queue
import socket
import struct
import threading
import time

IP_SERVER = '10.1.137.22'
Port_NM = 3114
Broadcast_NM = 8000 # Puerto correcto es el 5000

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

server.settimeout(0.2)
message = struct.pack("=BI", 5, 1000)
#message = b"your very important message"
server.sendto(message, ('<broadcast>', Broadcast_NM))
server.close()
print ("Ya me detuve de enviar Broadcast")

while True:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((IP_SERVER, Port_NM))
		s.listen()
		conn, addr = s.accept()
		time.sleep(1)
		data = 0
		with conn:
			print('Connected by', addr)
			try:
				data = conn.recv(692000) # Tamaño máximo de las páginas de todos los equipos
				if data[0] == 2:
					package_struct = "=B" + str(len(data) - 1) + "s"
					info = struct.unpack(package_struct, data)
					print ("Se realiza la operacion OK")
				if data[0] == 0:
					numero = struct.unpack("=I", data[6:10])
					ok_message = struct.pack("=B", 2)
					conn.sendall(ok_message)
					print (numero[0])
				if not data:
					break
				conn.sendall(data)
				# ~ time.sleep(2)
				s.close()
				time.sleep(1)
				
			except Exception:
				print("Me cerre antes de tiempo")
				s.close() 
				time.sleep(1)
