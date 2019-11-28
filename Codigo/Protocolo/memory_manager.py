#Imports
import pickle
import os
import team_interpreter
import sensor_interpreter
import time
import socket
import struct
#Imports

HOST = '127.0.0.1'
PORT = 2000        # The port used by the server

max_pages = 4
active_pages = 0
pages_list = {}

PRIMARY = 0
SECUNDARY = 1 

def create_page(page_id):
	global active_pages
	# ~ global pages_list
	print(str(active_pages))
	if(active_pages < 4):
		pages_list[page_id] = PageInfo()
		active_pages += 1
		return page_id
	else:
		print("No puede crear mas paginas")
	
#pageID como quinto argumento de lo de abajo
def store(date, teamId, sensorId, data, pageId):	
	team = str(team_interpreter.interpret(teamId))
	sensor = str(sensor_interpreter.interpret(sensorId))
	pageId1 = str(pageId)
	print(pageId1)
	folder_path = "./pages/" + team #Idea de carpeta por sensor equipo recolocar
	if(os.path.exists(folder_path)==False):
		os.makedirs(path)
	team_folder = os.path.join(folder_path, sensor + pageId1 + ".txt")
	
	if(os.path.exists(team_folder)!=False):	
		#path = path + sensor + pageId1 + ".txt"
		print("El documento existe")
		tamanio = os.stat(team_folder)
		print("EL TAMANIO REGISTRADO ES:        "+str(tamanio.st_size))

		if(int(tamanio.st_size) < 1024):
			if(active_pages < 4):
				file = open(str(team_folder), "a")
				file.write("%d" % int(date) + " " + "%f" % float(data) + " \n")
				file.close()
		else:
			print("Ocupo Swap")
			swap(team_folder)
	else:
		if(int(active_pages) < 4):
			file = open(str(team_folder), "a")
			file.write("%d" % int(date) + " " + "%f" % float(data) + " \n")
			file.close()
		else:
			print("Ocupo Swap")
			swap(team_folder)

def read(teamId, sensorId, pageId):
	vector = []
	team = team_interpreter.interpret(teamId)
	sensor = sensor_interpreter.interpret(sensorId)
	path = "./pages/" + team
	pageId1 = pageId + 1
	with open(path+sensor+str(pageId1)+".txt", "rt") as myfile:
		for myline in myfile:
			vector.append(myline)
	return vector

# with open('data.txt', 'r') as file:
#     data = file.read().replace('\n', '')

def swap(page_path):
	with open(page_path, 'r') as file:
		data = file.read.replace('\n', '')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))	
	package_format = "=BBI"
	packaged_data = struct.pack("S", data)
	package = struct.pack(package_format, 0, 1, 4)
	package += packaged_data
	
	s.sendall(package)
    data = s.recv(692000)
    print(str(data))
    
    time.sleep(2)
    
    package_format_2 = "=BB"
    package_2 = struct.pack(package_format_2, 1, 1)
    
    s.sendall(package_2)
    print("Mandé paquete lectura")
    data = s.recv(692000)
    print(str(data))
    information = struct.unpack("=I", data[2:6])
    print("La pagina que guarde es: " + str(information[0]))
        
    s.shutdown(1)
    s.close()


class PageInfo():
    def __init__(self, *args, **kwargs):
        self.size = 0
        self.content = []
		