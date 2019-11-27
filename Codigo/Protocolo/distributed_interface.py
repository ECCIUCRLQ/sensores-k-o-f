#import operationcode_interpreter
#import packer
import queue
import socket
import struct
import threading
import sys

distributed_page_table = {} #Dicccionario paginas
nodes_information = {} #Diccionario nodos

broadcast_direction = sys.argv[1]

ML_ID_PORT = 2000 # Corregir por 2000
ID_NM_PORT = 3114 # Corregir 3114
BROADCAST_NODE_PORT = 8000 #Corregir 5000

#MY_IP = '10.1.138.157' # Aquí va la dirección reservada K.O.F.
MY_IP = '127.0.0.1' 	# Aquí va la dirección reservada K.O.F.
IP_ML = '10.1.138.157' 	# Aquí va la dirección IP de la máquina con la ML
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
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((Direccion_IP, ID_NM_PORT))
		s.sendall(paquete)
		s.close()

def receive_page():
	global IP_NM
	
	# Server broadcast
	
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	client.bind((broadcast_direction, BROADCAST_NODE_PORT ))
	data, addr = client.recvfrom(1024)
	IP_NM = str(addr[0])
	print("Hola, recibí desde el puerto " + IP_NM)
	client.close() #Se acaba el broadcast
	
	tamano = struct.unpack("=I", data[1:5])
	print (tamano[0])
	nodes_information[IP_NM] = tamano[0]
	nodes_information['10.99.99.99'] =500
	for key, value in nodes_information.items() :
		print (key, value)
		
	# Termina logica broadcast
		
	if(data[0] == 5): # Caso de registro de nodo UDP (Por eso va al principio)
		paquete = struct.pack("=B", 2)
		ok_broadcast(paquete, IP_NM)
	
	# ~ while True:	
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((MY_IP, ML_ID_PORT))
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
						distributed_page_table[str(select_node(tamanio[0]))] = data[1]
						print("Despues de guardar id de pagina en diccionario")
						print(distributed_page_table[str(select_node(tamanio[0]))])
						info = struct.unpack(package_struct, data)
						print ("Page_Id: " + str(info[1]))
						paquete_ok_ml = envio_nm(data, select_node(tamanio[0])) # Busco la ip del nodo, y envio
						print("Se recibe paquete OK en ID: " + str(paquete_ok_ml))
						conn.sendall(paquete_ok_ml)
						print ("Se regresa de la subrutina envio_nm")
						s.close()
						print ("Ya me cerre")
						#data = s.recv(692000)
						#if(data[0] == 2):
						#	print ("Se recibio el OK")
					
					if data[0] == 1: # Se lee una pagina de memoria. Este es el paquete que envia de ID a NM
						print("Entre al if de lectura")
						page_id = data[1]
						used_ip = ""
						for ip, page in distributed_page_table.items():    #for name, age in dictionary.iteritems():  (for Python 2.x)
							if page == page_id:
								used_ip = ip
								break
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
	receive_page()
	print("Debugger")

main()
