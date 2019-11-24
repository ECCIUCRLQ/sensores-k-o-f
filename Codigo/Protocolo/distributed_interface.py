#HelloWorld
#import operationcode_interpreter
#import packer
import queue
import socket
import struct
import threading

BROADCAST_NODE_PORT = 6000

distributed_page_table = {}
nodes_information = {}

LOCAL_PORT = 2000

MY_IP = '192.168.1.40' #Aquí va la dirección reservada K.O.F.
IP_ML = '127.0.0.1' #Aquí va la dirección IP de la máquina con la ML
#De ML a NM
def store_page():
	page_size = 0
	node_ip = select_node()

def receive_page():
	#De NM a ML
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

#Se asegura de devolver el nodo con más espacio suficiente 
def select_node(page_size):
	node_ip = ''
	biggest_size = page_size
	for node_id in nodes_information:
		if nodes_information[node_id] >= biggest_size:
			biggest_size = nodes_information[node_id]
			node_ip = node_id
	#NO se contempla el caso donde ningún nodo tenga suficiente espacio
	return node_ip

def main():
	nodes_information['127.0.0.1'] = 1024