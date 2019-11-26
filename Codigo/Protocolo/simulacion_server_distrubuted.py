import socket
import struct

IP_ML = '127.0.0.1'
LOCAL_PORT = 2000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((IP_ML, LOCAL_PORT))
		s.listen()
		conn, addr = s.accept()
		#package_format = "B" + str(len(page_size)) + "s"
		with conn:
			print('Connected by', addr)
			try:
				while True:
					data = conn.recv(192706) # Tamaño máximo de las páginas de todos los equipos
					if data[0] == 0:
						package_struct = "B" + str(len(data) - 1) + "s"
						info = struct.unpack(package_struct, data)
						print ("El paquete fue recibido desde la ip " + "El string recibido es: " + str(info[1]))
					if data[0] == 1:
						print ("Se lee")  
					if not data:
						break
					conn.sendall(data)
			except Exception:
				s.close()