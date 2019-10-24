import socket
import time
import struct
import select
from ipcqueue import sysvmq

values = []
	
#UDP_IP = "10.1.137.90"
UDP_IP = "127.0.0.1"
UDP_PORT = 5005

time.sleep(5) # Test the client's timeout

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

q = sysvmq.Queue(2)
s = struct.Struct("BIBBBBBf")
ss = struct.Struct("BBBBB")
sss = struct.Struct("BIBBf")
while True:
    readable = select.select([sock],[],[],6)
    if readable[0]:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        values = s.unpack(data)
        dtime = time.ctime(values[1])
        #values[0] => Random(ACK)
        #values[1] => Time
        #values[2] => Team Id
        #values[3] => Sensor Id
        #values[4] => Sensor Id
        #values[5] => Sensor Id
        #values[6] => Data Tyoe
        #values[7] => Data
        print(str(values[0]) + " " + str(dtime) + " " + str(values[2]) + " " + str(values[3]) + " " + str(values[4]) + " " + str(values[5]) + " " + str(values[6]) + " " + str(values[7]))
        #if process( Team Id(values[2]).abierto)
        	#send()
        #else 
        	#Malloc-Maraviloso

        msm = ss.pack(values[0],values[2],values[3],values[4],values[5])
        sock.sendto(msm, (addr))
        values[0] = 0 
        sensors_info = sss.pack(values[0], values[1], values[2], values[3], values[7])
        q.put(sensors_info, msg_type=1)
    else:
        print ("Pi sensors are dead")

print("End of server")    
