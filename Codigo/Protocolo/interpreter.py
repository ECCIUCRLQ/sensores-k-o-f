from ipcqueue import sysvmq
import struct
import select
import time

q = sysvmq.Queue(2)
s = struct.Struct('BIBBBBBf')
value = 1
while True:
	data = q.get(block=True, msg_type=1)
	info = s.unpack(data)
	dtime = time.ctime(info[1])
	baseName = "Output"
	fileFormat = ".txt"
	fileName = baseName + str(value) + fileFormat
	f = open (fileName, "w")
	f.write(str(info[0]) + " "+ str(dtime) + " " + str(info[2]) + " " + str(info[3]) + " " + str(info[4]) + " " + str(info[5]) + " " + str(info[6]) + " " + str(info[7]) + "\n")
	f.close()
	value = value + 1
	
	
