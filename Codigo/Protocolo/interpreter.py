#Imports
from ipcqueue import sysvmq
import struct
import select
import time
import team_interpreter
import sensor_interpreter
#Imports

q = sysvmq.Queue(2)
s = struct.Struct('BIBBBBBf')

while True:
	data = q.get(block=True, msg_type=1)
	info = s.unpack(data)
	dtime = time.ctime(info[1])

	teamId = str(info[2])
	sensorType = str(info[5])

	#Block of code related to the teamId
	baseName = team_interpreter.interpret(teamId)
	
	#Block of code related to the sensorType
	sensorType == sensor_interpreter.interpret(sensorType)

	fileFormat = ".txt"
	fileName = baseName + fileFormat

	f = open (fileName, "a") #The option "a" makes sure that the new data does not erase the previous data
	f.write(str(info[0]) + " "+ str(dtime) + " " + baseName + " " + str(info[3]) + " " + str(info[4]) + " " + sensorType + " " + str(info[6]) + " " + str(info[7]) + "\n")
	f.close()
	
	# ~ value = value + 1
