import socket
from typing import NamedTuple
from time import time
from struct import *
import pickle
import random


class MessageClass(NamedTuple):
	randomID: int
	date: bytes
	sensorId: int
	sensorType: str
	boolData: bool
	floatData: float

randomID = random.randint(1,10)
packRandom = pack(">B", randomID)
curTime = int(time())
packTime = pack(">i", curTime)
sensorId = 41
packSensorId = pack(">B", sensorId)
MessageClass1 = MessageClass(packRandom,packTime,packSensorId,'CampoSensor',True,6.0)

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = pickle.dumps(MessageClass1)

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

checker = False

while not checker:
	sock.settimeout(1)
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	try:
		msm = sock.recvfrom(1024)
		checker = True
	except socket.timeout:
		print('I timed out.')

print(msm)
