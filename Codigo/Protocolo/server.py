import socket
from typing import NamedTuple
import time
import struct

values = []

#BiiBf
	
#UDP_IP = "10.1.137.90"
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
s = struct.Struct("BIBBBBBf")
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    values = s.unpack(data)
    dtime = time.ctime(values[1])
    print(str(values[0]) + " " + str(dtime) + " " + str(values[2]) + " " + str(values[3]) + " " + str(values[4]) + " " + str(values[5]) + " " + str(values[6]) + " " + str(values[7]))