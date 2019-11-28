# File system code. This file system configures a node to save n bytes
import logging
import math
import socket
import struct
import sys
import threading
import time

memory_size = int(sys.argv[1])
fixed_memory = int(sys.argv[1])
broadcast_direction = sys.argv[2]
memory_meta = 0
registered = False
Broadcast_NM = 5000 # Puerto correcto es el 5000
MY_IP = '' 			# Poner la ip de la maquina
Port_NM = 3114 		# Correcto

def broadcast_thread():
	global registered
	global Broadcast_NM
	global fixed_memory
	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server.settimeout(0.2)
	message = struct.pack("=BI", 5, fixed_memory)
	while not (registered):
		server.sendto(message, (broadcast_direction, Broadcast_NM))
		time.sleep(1)
	
	server.close()
	print("Se cerro la conexion UDP BC")
	
	
def transmission_thread():
	global memory_meta
	global memory_size
	global registered
	global Port_NM
	while True:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind((MY_IP, Port_NM))
			s.listen()
			conn, addr = s.accept()
			#package_format = "B" + str(len(page_size)) + "s"
			with conn:
				print('Connected by', addr)
				try:
					data = conn.recv(192706) # Tamaño máximo de las páginas de todos los equipos
					# ~ print(data)
					if(data[0] == 0): #Expected structure: Operation, ID_Page, Page_Size, Data
						#Meta structure: Page_ID, Size, Offset, Creation_Date, Consult_Date
						f = open("bin.txt", "rb+")
						f.seek(memory_meta)
						f.write((data[1]).to_bytes(1, "big")) #Escribe el page_Id
						file_size = struct.unpack("I", data[2:6]) #Recupera el tamanio de pagina
						# ~ print("Guardando, el tamano de pagina es " + str(file_size))
						# ~ print("Ademas, se escribe por la posicion " + str(memory_size))
						#f.seek(memory_size - file_size[0])
						f.write((file_size[0]).to_bytes(4, "little")) #Escribe tamanio de pagina
						offset = memory_size - file_size[0]
						# ~ print("Cuando escribo, el offset es" + str(offset))
						f.write((offset).to_bytes(4, "little"))
						f.write((int(time.time())).to_bytes(4, "little")) #Creation_Date
						f.write((int(time.time())).to_bytes(4, "little")) #Mod_Date
						memory_meta += 17
						f.seek(offset)
						# ~ print("Llegue hasta offset")
						for i in range(6,(file_size[0] + 6)):
							f.write((data[i]).to_bytes(1, "big"))
						memory_size = offset #change this to package size
						f.seek(4)
						f.write((memory_size).to_bytes(4,"big"))
						msm = struct.pack("=BBI", 2, data[1], (memory_size - memory_meta)) #Packs info
						conn.sendall(msm) # returns available memory
						# ~ f.seek(offset)
						# ~ informacion = struct.unpack("=I", f.read(4))
						# ~ print(informacion[0])
						# ~ print("Llegue hasta close")
						f.close()
						# ~ print("Pase el close")
						
					elif (data[0] == 1):
						print("Entro a lectura")
						print(data)
						f = open("bin.txt", "rb+")
						founded = False
						memory_counter = 8
						current_size = 0
						while (not founded) and memory_counter < memory_meta:
							print("Entro a while")
							f.seek(memory_counter)
							current_id = struct.unpack("=B", f.read(1))
							print("El id leido es " + str(current_id[0]))
							print("Data [1] es: " + str(data[1]))
							if(str(current_id[0]) == str(data[1])): #if page_id match
								print("Encontre pagina")
								founded = True
								f.seek(memory_counter + 1)
								#f.seek(memory_counter)
								print("Memory counter es:" + str(memory_counter))
								print("Me ubico en page_size")
								#byte_size = struct.unpack("=I", f.read(4)) #Reads size of page

								# print(str(f.read(4)))
								current_size = struct.unpack("=I", f.read(4))
								print("El tamano de la pagina de la lectura es: " + str(current_size[0]))
								#f.seek(memory_counter + 5)
								print("Me ubico en offset")
								byte_offset = struct.unpack("=I", f.read(4)) #Reads page offset
								print("Leo el offset")
								offset = byte_offset[0]
								print("Antes de ir a datos")
								#f.seek(offset)
								f.seek(offset)
								print("Me ubico en datos")
								print(offset)
								print("Se imprime el tamano a leer " + str(current_size[0]))
								#print(str(f.read(current_size[0])))
								#to_send = struct.unpack("=I", f.read(current_size[0])) #Maybe a byte Array here
								to_send = f.read(current_size[0])
								# tamanio_paquete = int(to_send[0])
								# print("Empaquete pagina" + str(to_send))
								# print(str(len(str(tamanio_paquete))))
								# package_format = "=BB" + str(len(str(tamanio_paquete))) + "s"
								# print("Pase el format maldito")
								# package = struct.pack(package_format, 3, data[1], int(to_send[0]))
								package = struct.pack("BB", 3, data[1])
								package += to_send
								f.seek(memory_counter + 12)
								f.write((int(time.time())).to_bytes(4, "little"))
								f.close()
								print(str(package))
								conn.sendall(package)
							else:
								memory_counter += 17 #If the id doesnt match, move the cursor
								
						if not founded:
							msm = struct.pack("BBI", 4, data[1], (memory_size - memory_meta)) #Packs info
							conn.sendall(msm) #returns available memory

						else:
							print("El id leido fue " + str(current_id))
								
					elif (data[0] == 2):
						registered = True
						
				except Exception:
					print("Termino antes")
def console_Thread():
	global memory_meta
	while(True):
		print("En caso de querer desplegar el listado de paginas, escriba ls")
		readed_value = str(input())
		if(readed_value == "ls"):
			f = open("bin.txt", "rb")
			id_counter = 8
			while(id_counter < memory_meta):
				f.seek(id_counter)
				value = int.from_bytes(f.read(1), "big")
				page_size = int.from_bytes(f.read(4), "little")
				f.seek(id_counter + 9)
				creation_date = time.ctime(int.from_bytes(f.read(4), "little"))
				consult_date = time.ctime(int.from_bytes(f.read(4), "little"))
				print("ID_Pagina\tTamano\tFecha Creacion\t\tFecha Consulta")
				print("% d\t\t%d\t%s\t%s" %(value, page_size, creation_date, consult_date))
				id_counter += 17
		

if (len(sys.argv)) == 3:	
	memory_meta = 0
	memory_meta = 8
	
	bin_file = open("bin.txt", "wb")
	bin_file.write((memory_meta).to_bytes(4, "big")) #Meta data is the first number of the binary file
	bin_file.write((memory_size).to_bytes(4, "big"))
	bin_file.close()
	
	threads = list()
	 
	logging.info("Main    : create and start thread %d.", 1)
	x = threading.Thread(target=broadcast_thread, args=())
	threads.append(x)
	x.start()
	
	logging.info("Main    : create and start thread %d.", 2)
	x = threading.Thread(target=transmission_thread, args=())
	threads.append(x)
	x.start()
	
	logging.info("Main    : create and start thread %d.", 3)
	x = threading.Thread(target=console_Thread, args=())
	threads.append(x)
	x.start()

	for index, thread in enumerate(threads):
		logging.info("Main    : before joining thread %d.", index)
		thread.join()
		logging.info("Main    : thread %d done", index)
        
	print("Weird finish")
	
else:
	print ("El uso de este programa es: python filesystem.py [bytes_disponibles]")
