from ipcqueue import sysvmq
import struct
import select
import time

q = sysvmq.Queue(2)
s = struct.Struct('BIBBBBBf')

while True:
	data = q.get(block=True, msg_type=1)
	info = s.unpack(data)
	dtime = time.ctime(info[1])

	teamId = str(info[2])
	sensorType = str(info[5])

	#Block of code related to the teamId
	if teamId == '1':
		baseName = "Whitenoise"
	elif teamId == '2':
		baseName = "FlamingoBlack"
	elif teamId == '3':
		baseName = "GISSO"
	elif teamId == '4':
		baseName = "KOF"
	elif teamId == '5':
		baseName = "Equipo404"
	elif teamId == '6':
		baseName = "Poffis"
	
	#Block of code related to the sensorType
	if sensorType == '1':
		sensorType = "Movimiento"
	elif sensorType == '2':
		sensorType = "Sonido (Big Sound)"
	elif sensorType == '3':
		sensorType = "Luz"
	elif sensorType == '4':
		sensorType = "Shock"
	elif sensorType == '5':
		sensorType = "Touch"
	elif sensorType == '6':
		sensorType = "Humedad"
	elif sensorType == '7':
		sensorType = "Big Sound"
	elif sensorType == '8':
		sensorType = "Temperatura"
	elif sensorType == '9':
		sensorType = "Ultrasonico"

	fileFormat = ".txt"
	fileName = baseName + fileFormat

	f = open (fileName, "a") #The option "a" makes sure that the new data does not erase the previous data
	f.write(str(info[0]) + " "+ str(dtime) + " " + baseName + " " + str(info[3]) + " " + str(info[4]) + " " + sensorType + " " + str(info[6]) + " " + str(info[7]) + "\n")
	f.close()
	
	# ~ value = value + 1
