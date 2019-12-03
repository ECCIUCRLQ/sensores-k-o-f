import struct
import socket
import time
#import packer

ID_PORT = 2000
ID_IP = ''
ID_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

num_pages = 0 #Los ID comienzan con 0, por un consejo de Marco y el buen Philip
page_table = [] #Voy a intentar que esto funcione como una Cola
local_memory = bytearray(4096)
page_size = 1024
pages = [] #Voy a intentar que esto funcione como una Pila

def conectar():
	is_disconected = True
	while is_disconected:
		try:
			ID_SOCKET.connect(ID_IP,ID_PORT)
			print("Conexion con el puerto: "+str(ID_PORT)+" establecida.")
			is_disconected = False
		except:
			print("Fallo en la conexion...")
			print("Nuevo intento en 3")
			time.sleep(1)
			print("Nuevo intento en 2")
			time.sleep(1)
			print("Nuevo intento en 1")
			time.sleep(1)
			print("Intentando de nuevo...")

def new_page():
	index = 0
	if memory_full():
		print("Swap")
	else:
		index = get_position()
	page_table.append(index)
	pages.insert(0, num_pages)
	page_id = num_pages
	num_pages+=1
	return page_id #Devuelve el ID de la Pagina que crea

def memory_full():
	if(len(pages)==4):
		return True
	return False	

def get_position(self):
	index = 0
	available = False
	while not available:
		if index in page_table:
			index += self.page_size
		else:
			available = True
	return index

def store_data(size, page_id, offset, data):
	print("Guardando un dato...")

def empty_page(self, index):
	for slot in range(index, index+self.page_size):
		self.local_memory[slot] = 0x00

def is_in_principal(self, id):
	if self.page_table[id] == -1:
		return False
	else:
		return True