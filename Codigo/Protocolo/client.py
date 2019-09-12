import socket
from typing import NamedTuple
from time import time
from struct import *
import pickle


class MessageClass(NamedTuple):
	randomID: int
	date: bytes
	sensorId: int
	sensorType: str
	boolData: bool
	floatData: float

curTime = int(time())
packTime = pack(">i", curTime)
MessageClass1 = MessageClass(1,packTime,3,'CampoSensor',True,6.0)
UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = pickle.dumps(MessageClass1)

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
