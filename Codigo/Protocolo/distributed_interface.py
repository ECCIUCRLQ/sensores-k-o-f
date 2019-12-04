#import operationcode_interpreter
#import packer
import queue
import select
import socket
import struct
import threading
import logging
import sys
import uuid
import time
from ipcqueue import sysvmq

distributed_page_table = {}	# Diccionario paginas
nodes_information = {} 		# Diccionario nodos

broadcast_direction = sys.argv[1]

ML_ID_PORT = 2000 			# Corregir 2000
ID_NM_PORT = 3114 			# Corregir 3114
ID_ID_PORT = 6666 			# Corregir 6666
BROADCAST_NODE_PORT = 8000 	# Corregir 5000

ACTIVE = False
buzon_de_hilos = queue.Queue(1)
semaforo_activa = threading.Semaphore()

#MY_IP = '10.1.138.157' # Aquí va la dirección reservada K.O.F.
MY_IP = '127.0.0.1' 	# Aquí va la dirección reservada K.O.F.
IP_ML = '10.1.137.101' 	# Aquí va la dirección IP de la máquina con la ML
IP_NM = '' 				# Esta será la dirección IP tomada del el broadcast

# De ML a NM
def store_page(page_size):
	node_ip = select_node(page_size)
	
# Se asegura de devolver el nodo con más espacio suficiente 
def select_node(page_size):
	node_ip = ''
	biggest_size = page_size
	for node_id in nodes_information:
		if nodes_information[node_id] >= biggest_size:
			biggest_size = nodes_information[node_id]
			node_ip = node_id
	# NO se contempla el caso donde ningún nodo tenga suficiente espacio
	return node_ip

# Esta será la subrutina que envía las páginas a NM
def envio_nm(paquete, Direccion_IP):
	# ~ global IP_NM
	# ~ used_IP = select_node(2) #Se 
	print(Direccion_IP)
	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((Direccion_IP, ID_NM_PORT))
		
		# ~ string_send = bytearray("Esto es un String de prueba" , 'utf-8')
		# ~ # string_send = b'Hello, world'
		# ~ package_format = "B" + str(len(string_send)) + "s"
		# ~ package = struct.pack(package_format, 0, string_send)
		# ~ #time.sleep(1)
		s.sendall(paquete)
		# ~ data = s.recv(192706)
		
		print ("envio_nm: Se espera confirmacion")
		data = s.recv(692000)
		print ("envio_nm: Se recibe confirmacion: " + str(data))
		if(data[0] != 5):
			if(data[0] == 2):
				print ("envio_nm: Se recibe OK")
				return data
			if(data[0] == 3):
				return data
			if(data[0] == 4):
				print ("envio_nm: No se encontro la pagina")
			
		#s.shutdown(1)
		s.close()
		
# Se usa una unica vez para confirmar al broadcast que ya sabe que esta vivo
def ok_broadcast(paquete, Direccion_IP):
	global ID_NM_PORT
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((Direccion_IP, ID_NM_PORT))
		s.sendall(paquete)
		print("NM conectado " + str(Direccion_IP))
		s.close()

# Se implementa el codigo propio de la competencia de todas las ID pasivas
def champions_mieo():
	global ACTIVE
	mac = uuid.getnode()
	perdi = False
	ronda_ID = 0
	timeout = time.time()+3
	
	while not ACTIVE and not perdi and time.time() < timeout :
		client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		client.settimeout(0.2)
		package_format = "=B"
		package = struct.pack(package_format, 0)
		package += mac.to_bytes(6, byteorder='big')
		ronda_ID_package = struct.pack("=B", ronda_ID)
		package += ronda_ID_package
		client.sendto(package, (broadcast_direction, ID_ID_PORT))
		client.close()
		
		server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		server.bind((broadcast_direction, ID_ID_PORT))
		readable = select.select([server], [], [], 2)
		if readable[0]:
			received = server.recvfrom(1024)
			if received[7] == ronda_ID:
				received_mac = struct.unpack("=l", received[1:7])
				if mac < received_mac:
					perdi = True
					
				else:
					ronda_ID += 1 #Se pelea la siguiente ronda
					
			elif received[7] > ronda_ID: # Caso en que mi ronda no es valida
				perdi = True
				
		else: # Si no recibo nada en el timeout
			ACTIVE = True
			
		client.close()

# Rutina cuando el distribuido 
def active_thread():
	global buzon_de_hilos 

	print("Me declaro como interfaz activa. Bomboclat rastaman.")

	semaforo_activa.release() # Se habilitan las subrutinas broadcast_thread y transmission_thread

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client.settimeout(0.2)
	while True:
		try:
			packet = buzon_de_hilos.get(block=True, timeout=2)
			client.sendto(packet, (broadcast_direction, ID_ID_PORT))

		except queue.Empty:
			packetStruct = "=BBBBB"
			packet = struct.pack(packetStruct, 2, 0, 0, 0, 0)
			client.sendto(packet, (broadcast_direction, ID_ID_PORT))

# Hilo que siempre se ejecutara cuando una ID quede como pasiva
def passive_thread():
	global ID_ID_PORT
	global ACTIVE

	server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	server.bind((broadcast_direction, ID_ID_PORT ))

	print("Se reciben paquetes de interfaces distribuidas")
	while not ACTIVE:
		readable = select.select([server], [], [], 4)
		if readable[0]:
			data, addr = server.recvfrom(692000)

			if(data[0] == 0 and ACTIVE):
				pass
			elif(data[0] == 1):
				filas1 = data[1]
				filas2 = data[2]

				dump1 = filas1*2
				datos_tabla_paginas = data[3:(3+dump1)]
				for index in range(0, filas1, 2):
					distributed_page_table[data[3+index]] = data[3+index+1]

				dump2 = filas2*9
				datos_tabla_nodos = data[(3+dump1):(3+dump1+dump2)]
				for index in range(0, filas2, 9):
					nodes_information[data[3+index+dump1+1]] = data[3+index+dump1+5]
			elif(data[0] == 2):
				filas1 = data[1]
				if(filas1 != 0):
					filas2 = data[2]

					dump1 = filas1*2
					datos_tabla_paginas = data[3:(3+dump1)]
					for index in range(0, filas1, 2):
						distributed_page_table[data[3+index]] = data[3+index+1]

					dump2 = filas2*9
					datos_tabla_nodos = data[(3+dump1):(3+dump1+dump2)]
					for index in range(0, filas2, 9):
						nodes_information[data[3+index+dump1+1]] = data[3+index+dump1+5]
		else:
			champions_mieo()
	server.close()
	active_thread()

def broadcast_thread():
	global semaforo_activa
	global broadcast_direction
	global BROADCAST_NODE_PORT

	semaforo_activa.acquire() # Hasta que sea una interfaz activa se corre esto

	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	client.bind((broadcast_direction, BROADCAST_NODE_PORT ))
	
	print("Se empieza a recibir por udp")

	data, addr = client.recvfrom(692000)
	IP_NM = str(addr[0])
	print("Hola, recibí desde el puerto " + IP_NM)
	client.close() #Se acaba el broadcast
	
	tamano = struct.unpack("=I", data[1:5])
	print (tamano[0])
	nodes_information[IP_NM] = tamano[0]

	if(data[0] == 5): # Caso de registro de nodo UDP (Por eso va al principio)
		paquete = struct.pack("=B", 2)
		ok_broadcast(paquete, IP_NM)

# Empaquetar en cola para hacer broadcast de tabla a pasivas
def transmission_thread():
	# ~ while True:	
	global buzon_de_hilos
	global semaforo_activa

	semaforo_activa.acquire() # Hasta que sea una interfaz activa se corre esto

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((IP_ML, ML_ID_PORT)) # Direccion mia como servidor
		print("Abri socket")
		s.listen()
		conn, addr = s.accept()
		print("Accept")
		#package_format = "B" + str(len(page_size)) + "s"
		with conn:
			print('Connected by', addr)
			while True:
				try:
					print("Empezando a recibir")
					data = conn.recv(692000) # Tamaño máximo de las páginas de todos los equipos
					print("Recibe algo: " + str(data))
					if data[0] == 0: # Guardar pagina. Pasar esta parte a nodo de memoria. Cola interprocesos
						package_struct = "=BBI" + str(len(data) - 6) + "s" # Me envian la pagina
						tamanio = struct.unpack("=I", data[2:6])
						print("Antes de guardar id de pagina en el diccionario")
						distributed_page_table[str(data[1])]=str(addr[0]) # Agrega ID Pagina como Key y Guarda el ip
						print("Despues de guardar id de pagina en diccionario")
						#print(distributed_page_table[str(select_node(tamanio[0]))])
						info = struct.unpack(package_struct, data)
						print ("Page_Id: " + str(info[1]))
						paquete_ok_ml = envio_nm(data, select_node(tamanio[0])) # Busco la ip del nodo, y envio
						print("Se recibe paquete OK en ID: " + str(paquete_ok_ml))
						conn.sendall(paquete_ok_ml)
						print ("Se regresa de la subrutina envio_nm")
						s.close()
						print ("Ya me cerre")
						
						# Se crean los dump que seran usados para los nodos de memoria
						dump1 = bytearray()
						dump2 = bytearray()
						
						# Se agregan los datos de la tabla de paginas al dump1
						for page in distributed_page_table:
							dump1.append(page) # lea page como id
							dump1.append(distributed_page_table[page]) # Agrega el valor
						
						# Se agregan los datos de la tabla de nodos al dump2
						id_node = 0
						for node in nodes_information:
							id_node += 1
							id_node_info = struct.pack("B", id_node)
							dump2.append(id_node_info[0]) # Agrega el id_node como identificador
							dump2.append(node)
							node_info = nodes_information[node]

							ip_node = struct.pack("I", node)
							size_node = struct.pack("I", node_info)

							for i in range(4):
								dump2.append(ip_node[i])

							for i in range(4):
								dump2.append(size_node[i])
						
						# Se obtienen las filas para generar el paquete de copia
						filas1 = len(distributed_page_table)
						filas2 = len(nodes_information)
						
						# Requiere revisión
						buzon_struct = "=BBB"
						buzon_packet = struct.pack(buzon_struct, 2, filas1, filas2)
						buzon_packet += dump1
						buzon_packet += dump2
						buzon_de_hilos.put(buzon_packet)

						#data = s.recv(692000)
						#if(data[0] == 2):
						#	print ("Se recibio el OK")
					
					if data[0] == 1: # Se lee una pagina de memoria. Este es el paquete que envia de ID a NM
						print("Entre al if de lectura")
						page_id = data[1]
						used_ip = ""
						for id in distributed_page_table:
							if str(id) == str(page_id):
								used_ip = distributed_page_table.get(id)
								break
						# for i in range(0,len(distributed_page_table_values)):
						# 	if(str(distributed_page_table_values[i]) == str(page_id)):
						# 		used_ip = distributed_page_table_ip[i]
						# 		break
						#for ip, page in distributed_page_table.items(): #for name, age in dictionary.iteritems():  (for Python 2.x)
							#print("Pagina es: " + str(page) + " con IP: " + str(ip))
							#print(str(page))
							#print(str(page_id))
							#if str(page) == str(page_id):
								#print("Si es la ip que encontre")
								#used_ip = ip
								#break
						print("IP es: " + str(used_ip))
						paquete_lectura_nm = struct.pack("=BB", data[0], data[1])
						paquete_regreso_ml = envio_nm(paquete_lectura_nm, used_ip)
						conn.sendall(paquete_regreso_ml)
						s.close()
					#if not data:
						#conn.sendall(data)
						#break
				except Exception:
					s.close()
					print("Esta brincando la Excepcion")

def main():	
	#nodes_information['127.0.0.1'] = 1024
	threads = list()
	 
	logging.info("Main    : create and start thread %d.", 1)
	x = threading.Thread(target=broadcast_thread, args=())
	threads.append(x)
	x.start()
	
	logging.info("Main    : create and start thread %d.", 2)
	x = threading.Thread(target=transmission_thread, args=())
	threads.append(x)
	x.start()

	# Este hilo corre comportamiento pasivo, activo y Champions
	logging.info("Main    : create and start thread %d.", 3)
	x = threading.Thread(target=passive_thread, args=())
	threads.append(x)
	x.start()

	for index, thread in enumerate(threads):
		logging.info("Main    : before joining thread %d.", index)
		thread.join()
		logging.info("Main    : thread %d done", index)
        
	print("Weird finish")

	print("Debugger")

main()
