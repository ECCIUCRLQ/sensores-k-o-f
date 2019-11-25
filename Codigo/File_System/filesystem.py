#File system code. This file system configures a node to save n bytes
import sys 
import math
from time import time
import socket

memory_size = int(sys.argv[1])
fixed_memory = int(sys.argv[1])
	

if (len(sys.argv)) == 2:	
	memory_meta = 0
	UDP_IP = "127.0.0.1"
	UDP_PORT = 5007
	operation = 0 #Zero means save a file
	
	#Sockets code
	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	
	memory_meta = 8
	bin_file = open("bin.txt", "wb")
	bin_file.write((memory_meta).to_bytes(4, "big")) #Meta data is the first number of the binary file
	bin_file.write((memory_size).to_bytes(4, "big"))
	bin_file.close()
	
	
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
				for i in range(6:(file_size + 6)):
					f.write((data[i]).to_bytes(1, "big"))
				f.close()
				memory_size = offset #change this to package size
				f.seek(4)
				f.write((memory_size).to_bytes(4,"big"))
				msm = struct.pack("BBI", 0, data[1], (memory_size - memory_meta)) #Packs info
				sock.sendto(msm, (addr)) #returns available memory
			elif (data[0] == 1):
				f = open("bin.txt", "rb+")
				founded = False
				memory_counter = 8
				current_size = 0
				while !founded and counter < memory_meta:
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
						package = struct.pack(package_format, data[1], string_send)
						sock.sendto(package, (addr))
					else:
						memory_counter += 17 #If the id doesnt match, move the cursor
						
						
				
			else:
				pass
				
	
	
else:
	print "El uso de este programa es: python filesystem.py [bytes_disponibles]"

