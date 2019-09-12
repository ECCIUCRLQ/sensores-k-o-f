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
	
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    MessageClass1 = pickle.loads(data)
    print(str(unpack(">B", MessageClass1.randomID)) + str(MessageClass1.sensorType))
