from socket import *
import socket
# ~ from typing import NamedTuple
from time import time
#import time
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

checker = False

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

# ~ while not checker:
	# ~ sock.settimeout(1)
	# ~ sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	# ~ try:
		# ~ msm = sock.recvfrom(1024)
		# ~ checker = True
	# ~ except socket.timeout:
		# ~ print('I timed out.')

# ~ print(msm)

	msm, addr = sock.recvfrom(1024)
	print(str(msm[0])+ " " + str(msm[1]) + " " + str(msm[2]) + " " + str(msm[3]))  #IDK if it already necessary 


	sockrecv = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


	while not checker:
		try:
			sockrecv.settimeout(1)
			data = sockrecv.recv(4096)
			checker = True

		except Exception as err:
			sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
			print("Time Error")
