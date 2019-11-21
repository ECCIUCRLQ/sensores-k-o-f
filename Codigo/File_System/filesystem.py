#File system code. This file system configures a node to save n bytes
import sys 
import math
from time import time
import socket

memory_size = 0

def init(size_of_memory):
	global memory_size
	memory_size = size_of_memory
	

if (len(sys.argv)) == 2:	
	memory_meta = 0
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5007
	operation = 0 #Zero means save a file
	
	#Sockets code
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	
	bin_file = open("bin.txt", "wb")
	bin_file.write((memory_meta).to_bytes(4, "big")) #Meta data is the first number of the binary file
	bin_file.write((memory_size).to_bytes(4, "big"))
	bin_file.close()
	memory_meta = 8
	
	
	#Socket loop 
	while(memory_size > memory_meta):
		readable = select.select([sock],[],[],6)
		#In case that an operation is received
		if readable[0]:
			data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
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
				for i in range(6:(file_size + 5)):
					f.write((data[i]).to_bytes(1, "big"))
				f.close()
				memory_size = offset #change this to package size
				msm = memory_size - 4
				#sock.sendto(msm, (addr)) returns available memory
				
			else:
				#read file
				
	
	
else:
	print "El uso de este programa es: python filesystem.py [bytes_disponibles]"

