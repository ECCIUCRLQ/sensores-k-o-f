import socket
from typing import NamedTuple
from time import time
#import time
import struct
import random

sensorId = [0x00,0x01,0x02]
#values = (randomId, date, sensorId, sensorType, data)
values = []
values.append(random.randint(1,10))
values.append(int(time()))
values.append(1) #TeamID
values.append(1)
values.append(0)

s = struct.Struct('BIBBBBBf')
pack = s.pack(values[0],values[1],values[2],sensorId[0],sensorId[1],sensorId[2],values[3],values[4])
#UDP_IP = "127.0.0.1"
UDP_IP = "10.1.137.102"
UDP_PORT = 10000
MESSAGE = pack

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

msm, addr = sock.recvfrom(1024)
print(str(msm[0])+ " " + str(msm[1]) + " " + str(msm[2]) + " " + str(msm[3]))