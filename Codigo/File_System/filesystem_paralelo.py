#File system code. This file system configures a node to save n bytes
import sys 
import math
from time import time
import socket
import threading

memory_size = int(sys.argv[1])
fixed_memory = int(sys.argv[1])
memory_meta = 0
registered = False
Broadcast_NM = 8000 # Puerto correcto es el 5000
MY_IP = '' #Poner la ip de la maquina
Port_NM = 3114 #Correcto

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
		server.sendto(message, ('<broadcast>', Broadcast_NM))
		time.sleep(1)
	
	server.close()
	
	
def transmission_thread():
	global memory_meta
	global memory_size
	global registered
	while True:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			s.bind((MY_IP, ML_ID_PORT))
			s.listen()
			conn, addr = s.accept()
			#package_format = "B" + str(len(page_size)) + "s"
			with conn:
				print('Connected by', addr)
				try:
					data = conn.recv(192706) # Tamaño máximo de las páginas de todos los equipos
					if(data[0] == 0): #Expected structure: Operation, ID_Page, Page_Size, Data
						#Meta structure: Page_ID, Size, Offset, Creation_Date, Consult_Date
						f = open("bin.txt", "rb+")
						f.seek(memory_meta)
						f.write((data[1]).to_bytes(1, "big"))
						file_size = struct.unpack("I", data[2:6])
						f.write((file_size).to_bytes(4, "big"))
						offset = memory_size - file_size
						f.write((offset).to_bytes(4, "big"))
						f.write((int(time.time())).to_bytes(4, "big")) #Creation_Date
						f.write((int(time.time())).to_bytes(4, "big")) #Mod_Date
						memory_meta += 17
						f.seek(offset)
						for i in range(6:(file_size + 6)):
							f.write((data[i]).to_bytes(1, "big"))
						f.close()
						memory_size = offset #change this to package size
						f.seek(4)
						f.write((memory_size).to_bytes(4,"big"))
						msm = struct.pack("BBI", 2, data[1], (memory_size - memory_meta)) #Packs info
						sock.sendto(msm, (addr)) #returns available memory
					
					elif (data[0] == 1):
						f = open("bin.txt", "rb+")
						founded = False
						memory_counter = 8
						current_size = 0
						while (not founded) and counter < memory_meta:
							f.seek(memory_counter)
							current_id = f.read(1)
							if(current_id == data[1]): #if page_id match
								founded = True
								f.seek(counter + 1)
								byte_size = f.read(4) #Reads size of page
								current_size = struct.unpack("I", byte_size)
								f.seek(counter + 5)
								byte_offset = f.read(4) #Reads page offset
								offset = struct.unpack("I", byte_offset)
								f.seek(offset)
								to_send = f.read(current_size) #Maybe a byte Array here
								package_format = "=BB" + str(len(to_send)) + "s"
								package = struct.pack(package_format, 3, data[1], string_send)
								sock.sendto(package, (addr))
							else:
								memory_counter += 17 #If the id doesnt match, move the cursor
								
						if not founded:
							msm = struct.pack("BBI", 4, data[1], (memory_size - memory_meta)) #Packs info
							sock.sendto(msm, (addr)) #returns available memory
								
					elif (data[0] == 2):
						registered = True
					

def console_Thread():
	print("Hacer")
		

if (len(sys.argv)) == 2:	
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
	print "El uso de este programa es: python filesystem.py [bytes_disponibles]"
