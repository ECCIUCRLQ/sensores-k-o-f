#import operationcode_interpreter
#import packer
import queue
import socket
import struct
import threading

distributed_page_table = {} #Dicccionario paginas
nodes_information = {} #Diccionario nodos

ML_ID_PORT = 2000 # Corregir por 2000
ID_NM_PORT = 3115 # Corregir 3114
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
		
		data = s.recv(692000)
		if(data[0] == 2):
			print ("Se recibio el ok. Vamonos")
			
		#s.shutdown(1)
		s.close()

def receive_page():
	global IP_NM
	
	#Server broadcast
	
	client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP
	client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
	client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

	client.bind(("", BROADCAST_NODE_PORT ))
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
		
	#Termina logica broadcast
		
	if(data[0] == 5): # Caso de registro de nodo UDP (Por eso va al principio)
		paquete = struct.pack("=B", 2)
		envio_nm(paquete, IP_NM)
		
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind((MY_IP, ML_ID_PORT))
		s.listen()
		conn, addr = s.accept()
		#package_format = "B" + str(len(page_size)) + "s"
		with conn:
			print('Connected by', addr)
			try:
				while True:
					data = conn.recv(192706) # Tamaño máximo de las páginas de todos los equipos
					if data[0] == 0: #Guardar pagina # Pasar esta parte a nodo de memoria. Cola interprocesos
						distributed_page_table[str(addr[0])] = data[1]
						print(distributed_page_table[str(addr[0])])
						package_struct = "=BBI" + str(len(data) - 6) + "s" # Me envian la pagina
						tamanio = struct.unpack("=I", data[2:6])
						info = struct.unpack(package_struct, data)
						print ("El paquete fue recibido desde la ip " + "El string recibido es: " + str(info[1]))
						envio_nm(data, select_node(tamanio[0])) # Busco la ip del nodo, y envio
						data = s.recv(692000)
						if(data[0] == 2):
							print ("Se recibio el ok. Vamonos")
					
					if data[0] == 1: #Se lee una pagina de memoria. Este es el paquete que envia de ID a NM
						page_id = data[1]
						for ip, page in distributed_page_table.items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
							if page == page_id:
								used_ip = ip
								break
								
						envio_nm(paquete, used_ip)
						 
					if not data:
						break
					conn.sendall(data)
			except Exception:
				s.close() 
	
	

def main():	
	# ~ nodes_information['127.0.0.1'] = 1024
	receive_page()
	print("Debugger")

main()
