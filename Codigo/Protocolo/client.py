from socket import *
import socket
from ipcqueue import sysvmq
# ~ from typing import NamedTuple
from time import time
#import time
import struct
import random
import select


sensorId = [0x00,0x01,0x02]
values = []
values.append(random.randint(0,255))
values.append(int(time()))
values.append(4) #TeamID

q = sysvmq.Queue(1)
s = struct.Struct('BIBBBBBf')
sensorData = struct.Struct('BBf')

UDP_IP = "127.0.0.1"
#UDP_IP = "10.1.137.67"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

checker = False

while True:
	checker = False
	packet = q.get(block=True, msg_type=1)
	packArray = sensorData.unpack(packet)
	values[0] = random.randint(0,255)
	values[1] = int(time())
	pack = s.pack(values[0],values[1],values[2],sensorId[0],sensorId[1],packArray[0],packArray[1],packArray[2])
	MESSAGE = pack

	print ("UDP target IP:", UDP_IP)
	print ("UDP target port:", UDP_PORT)
	print ("message:", MESSAGE)
	 
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


	while not checker:
		try:			
			readable = select.select([sock], [] , [] , 1)
			if readable[0]:
				data = sock.recv(4096)
				ss = struct.Struct("BBBBB")
				securityPack = ss.unpack(data)
				checker = True

			if not checker:
				sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

		except Exception: 
			continue
			
			
	print("End of while True")

print("EOR")
