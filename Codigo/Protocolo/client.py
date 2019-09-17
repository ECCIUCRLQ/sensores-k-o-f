import socket
# ~ from typing import NamedTuple
from time import time

import struct
import random
import select
from ipcqueue import sysvmq


sensorId = [0x00,0x01,0x02]
#values = (randomId, date, sensorId, sensorType, data)
values = []
values.append(random.randint(0,255))
values.append(int(time()))
values.append(1) #TeamID
values.append(1)
values.append(0)

q = sysvmq.Queue(1)
s = struct.Struct('BIBBBBBf')
while True:
	values[4] = q.get(block=True, msg_type=1)
	pack = s.pack(values[0],values[1],values[2],sensorId[0],sensorId[1],sensorId[2],values[3],values[4])
	UDP_IP = "127.0.0.1"
	#UDP_IP = "10.1.137.67"
	UDP_PORT = 5005
	MESSAGE = pack

	print ("UDP target IP:", UDP_IP)
	print ("UDP target port:", UDP_PORT)
	print ("message:", MESSAGE)

	sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

	#msm = sock.recvfrom(1024)
	#print(msm)


	sockrecv = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


	
	try:
		sockrecv.settimeout(1)
		data = sockrecv.recv(4096)



	except Exception as err:
		sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
		print("Time Error")
    
