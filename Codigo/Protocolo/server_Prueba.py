import queue
import socket
import struct
import threading

IP_SERVER = '127.0.0.1'
Port_NM = 3114



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((IP_SERVER, Port_NM))
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			try:
				while True:
					data = conn.recv(192706) # Tamaño máximo de las páginas de todos los equipos
					if data[0] == 0:
						package_struct = "=B" + str(len(data) - 1) + "s"
						info = struct.unpack(package_struct, data)
						print ("El paquete fue recibido desde la ip " + "El string recibido es: " + str(info[1]))
					if data[0] == 1:
						print ("Se lee")  
					if not data:
						break
					conn.sendall(data)
			except Exception:
				s.close() 
