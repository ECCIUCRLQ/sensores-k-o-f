import struct
import socket
import time
import Codigo.Protocolo.pack_manager as packer

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

def new_page(self):
	index = 0
	if memory_full():
		old_page = self.pages.pop()
		index = self.page_table[old_page]
		self.send_to_secundary(old_page)
	else:
		index = get_position()
	self.page_table.append(index)
	self.pages.insert(0, num_pages)
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

def store_data(self, size, page_id, offset, data):
	print("Guardando un dato...")
	if(is_in_principal(page_id)):
		index = self.page_table[page_id]
	else:
		index = swap(page_id)
	index += offset
	dis = 5 #Desplazamiento de 5 bytes
	for i in range(index, index+dis):
		self.local_memory[i] = data[i-index]
	if offset >= 1019:
		print("La pagina esta casi llena, se va a mandar a memoria secundaria")
		self.send_to_secundary(page_id)

def send_to_secundary(self, page_id):
	print("Enviando a secundaria...")
	sended_page = bytearray(self.page_size)
	index = self.page_table[page_id]
	for i in range(len(sended_page)):
		sended_page[i] = self.local_memory[index+i]
	pack = packer.store_package(0,page_id,self.page_size,sended_page)
	
	no_page = True
	while no_page:
		self.ID_SOCKET.send(pack)
		response = bytearray()
		received = self.ID_SOCKET.recv(692000)
		response += received
		control = packer.unpack_store_ID_NM(response, page_id)
		if(control == 0):
			no_page = False
		else:
			print("Reenviando...")
			time.sleep(3)
	print("La pagina se envio")
	self.page_table[page_id] = -1
	self.pages.remove(page_id)
	self.empty_page(index)	


def empty_page(self, index):
	for slot in range(index, index+self.page_size):
		self.local_memory[slot] = 0x00

def is_in_principal(self, id):
	if self.page_table[id] == -1:
		return False
	else:
		return True

def swap(self, page_id):
	index = self.get_position()
	self.get_secundary_page(page_id, index)
	self.pages.insert(0, page_id)

	return index

def read_data(self, index, data_size):
	print("Leyendo...")
	readed_data = bytearray(data_size)
	for i in range(data_size):
		readed_data[i] = self.local_memory[index+i]
	unpacked_data = struct.unpack("=If", readed_data)
	return unpacked_data[0], unpacked_data[1]

def get_page(self, page_id):
	page = []
	index = 0
	data_size = 5
	if(self.is_in_principal(page_id)):
		index = self.page_table[page_id]
	else:
		index = self.swap(page_id)
	for i in range (index, index+self.page_size, data_size):
		date, data = self.read_data(index, data_size)
		page.append(date)
		page.append(data)
	self.page_table[page_id] = -1
	self.pages.remove(page_id)
	self.empty_page(index)
	
	return page

def get_secundary_page(self, page_id, index):
	new_page = bytearray(1)
	page_packet = packer.read_package_store_ok(1,page_id)

	no_page = True

	while no_page:
		self.ID_SOCKET.sendall(page_packet)
		responce = bytearray()
		receive = self.ID_SOCKET.recv(692000)
		responce += receive
		new_page = packer.unpack_read_response(responce,page_id,self.page_size)
		if(new_page != 1):
			no_page = False
	for i in range(index, index + self.page_size):
		self.local_memory[i] = new_page[i-index]
	self.page_table[page_id] = index

	def main(self):
		self.conectar()
	main()