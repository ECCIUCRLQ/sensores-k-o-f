import sys
import time
import struct
import select
import matplotlib.pyplot as plt
import numpy as np
from ipcqueue import sysvmq

def hourInfo(hours, length, dataType):
	exteriorIndex = 0 #itera en packArray
	interiorIndex = 0 #itera en hours y length
	if dataType == 2:
		#floatCounter = 0.0
		floatTimes = []
		
	elif dataType == 3:
		#intCounter = 0
		intTimes = []
		
	while(exteriorIndex < len(packsArray)):
		timePack = str(time.ctime(packsArray[indice])).split(" ") #Se pone en un string cada parte de la fecha
		if(len(hours) == 0): #En caso de que sea la primera hora que se agrega
			splitTime = timePack[3].split(":")
			hours.append(splitTime[0]) #Se saca solo la hora
			if (dataType == 1):
				length.append(1)
			
			elif (dataType == 2):
				#floatCounter++
				length.append(packsArray[exteriorIndex + 1]) 
				floatTimes.append(1)
				
			elif (dataType == 3):
				#intCounter++
				length.append(packsArray[exteriorIndex + 1]) 
				intTimes.append(1)
			
			#hours[internalIndex] = '11'
			#splitTime[0] = '11'
			#No hay que agregar una nueva hora en hours y se suma 1 en length[internalIndex]
			
		else:
			splitTime = timePack[3].split(":") 
			if dataType == 1:
				if(splitTime[0] == hours[interiorIndex]):
					length[interiorIndex] += 1
					
				else:
					interiorIndex += 1
					hours[interiorIndex - 1] = hours[interiorIndex - 1] + ":00"
					hours.append(splitTime[0])
					length.append(1)
			
			elif dataType == 2:
				
				if(splitTime[0] == hours[interiorIndex]):
					#floatCounter++
					length[interiorIndex] += packsArray[exteriorIndex + 1]
					floatTimes[interiorIndex] += 1
					
				else:
					interiorIndex += 1
					hours[interiorIndex - 1] = hours[interiorIndex - 1] + ":00"
					float
					hours.append(splitTime[0])
					length.append(1)
					floatTimes.append(1)
			
			elif dataType == 3:
				
				if(splitTime[0] == hours[interiorIndex]):
					#floatCounter++
					length[interiorIndex] += packsArray[exteriorIndex + 1]
					intTimes[interiorIndex] += 1
					
				else:
					interiorIndex += 1
					hours[interiorIndex - 1] = hours[interiorIndex - 1] + ":00"
					float
					hours.append(splitTime[0])
					length.append(1)
					intTimes.append(1)
				
		exteriorIndex += 2
	
	if dataType == 2:
		for floatIndex in range(0, len(hours)):
			length[floatIndex] /= float(floatTimes[floatIndex])
			
	if dataType == 3:
		for intIndex in range(0, len(hours)):
			length[intIndex] /= intTimes[intIndex]
# ~ if len(sys.argv) >= 2:
	# ~ q = sysvmq.Queue(16)
	# ~ s = struct.Struct("I")
	# ~ ss = struct.Struct("I")
	# ~ if sys.argv[1] == '1': #Whitenoise graphics
		# ~ data = ss.pack(1)
		# ~ q.put(data, msg_type=1)
		# ~ dataArray = []
		# ~ receive = q.get(block=True, msg_type=1)
		# ~ sizePack = ss.unpack(receive)
		# ~ writeData = []
		
		# ~ for x in range(0, sizePack):
			# ~ receivedMsg = q.get(block=True, msg_type=1)
			# ~ #AQUI VA EL UNPACK
			# ~ unpackedData = []
			# ~ dataArray = dataArray + unpackedData
		# ~ for i in range(0, len(dataArray)):
			# ~ if i % 7 == 0 && i != 0:
				# ~ writeData.append("\n")
				
			# ~ writeData.append(str(dataArray[i]))
		
		# ~ npWrite = np.asarray(writeData)
		# ~ numpy.savetxt("foo.csv", a, delimiter=",")
			
	# ~ elif sys.argv[1] == '2': #FlamingoBlack sensors
		# ~ data = ss.pack(2)
		# ~ q.put(data, msg_type=1)
	# ~ elif sys.argv[1] == '3': #GISSO sensors
		# ~ data = ss.pack(3)
		# ~ q.put(data, msg_type=1)
	# ~ elif sys.argv[1] == '4': #KOF sensors
		# ~ data = ss.pack(4)
		# ~ q.put(data, msg_type=1)
	# ~ elif sys.argv[1] == '5': #404 sensors
		# ~ data = ss.pack(5)
		# ~ q.put(data, msg_type=1)
	# ~ elif sys.argv[1] == '6': #Poffis sensors
		# ~ print "Poffis seleccionado"
		# ~ data = ss.pack(6)
		# ~ q.put(data, msg_type=1)
	# ~ else: 
		# ~ print "Grupo desconocido\n"
		
# ~ else: 
	# ~ print "El uso de graphics es python graphics.py [IDGrupo]\n"
	
if len(sys.argv) == 3: # Contiene el numero de grupo y el numero de sensor
	q = sysvmq.Queue(16)
	s = struct.Struct("II")
	ss = struct.Struct("II")
	dataType = 0
	graphicsName = ["Whitenoise Movimiento", "Whitenoise Big Sound", "Flamingo Movimiento", "Flamingo Fotoresistor", 
		"Gisso Movimiento", "Gisso Shock", "KOF Movimiento", "KOF Touch", "404 Movimiento", "404 Humedad", "404 Temperatura", 
		"Poffis Humedad", "Poffis Big Sound"]
		
	if((sys.argv[2] == '6' or sys.argv[2] == '8') and (sys.argv[1] == '5')):
		dataType = 2 #Float data type
		
	elif (sys.argv[2] == '1' or sys.argv[2] == '2' or sys.argv[2] == '3' or sys.argv[2] == '4' or sys.argv[2] == '5') and (sys.argv[1] == '1' or sys.argv[1] == '2' or sys.argv[1] == '3' or sys.argv[1] == '4' or sys.argv[1] == '5'):
		dataType = 1 #Boolean data type
		
	elif((sys.argv[2] == '7' or sys.argv[2] == '9' ) and (sys.argv[1] == '6')):
		dataType = 3 #Integer data type
		
	if (dataType > 0 and dataType < 3):
		data = ss.pack(int(sys.argv[1]))
		q.put(data, msg_type=1)
		receive = q.get(block=True, msg_type=1)
		numPages = s.unpack(receive)
		numData = numPages * 1024 / 8
		packsArray = []
		for x in range(0, numData):
			receive = q.get(block=True, msg_type=1)
			receivedData = ss.unpack(receive)
			packsArray.append(receivedData[0]) #Date
			packsArray.append(receivedData[1]) #Data
			
		hour = []
		length = []
		hourInfo(hours, length, dataType)
		y_pos = np.arange(len(hour))
		plt.barh(y_pos, length, align='center', alpha = 100)
		plt.xticks(y_pos, hour)
		plt.ylabel('Frecuencia')
		if (sys.argv[1] == '1' and sys.argv[2] == '1'):
			plt.title(graphicsName[0])
			
		elif (sys.argv[1] == '1' and sys.argv[2] == '2'):
			plt.title(graphicsName[1])
			
		elif (sys.argv[1] == '2' and sys.argv[2] == '1'):
			plt.title(graphicsName[2])
			
		elif (sys.argv[1] == '2' and sys.argv[2] == '3'):
			plt.title(graphicsName[3])
			
		elif (sys.argv[1] == '3' and sys.argv[2] == '1'):
			plt.title(graphicsName[4])
			
		elif (sys.argv[1] == '3' and sys.argv[2] == '4'):
			plt.title(graphicsName[5])
			
		elif (sys.argv[1] == '4' and sys.argv[2] == '1'):
			plt.title(graphicsName[7])
			
		elif (sys.argv[1] == '4' and sys.argv[2] == '5'):
			plt.title(graphicsName[8])
			
		elif (sys.argv[1] == '5' and sys.argv[2] == '1'):
			plt.title(graphicsName[9])
			
		elif (sys.argv[1] == '5' and sys.argv[2] == '6'):
			plt.title(graphicsName[10])
			
		elif (sys.argv[1] == '5' and sys.argv[2] == '8'):
			plt.title(graphicsName[11])
			
		elif (sys.argv[1] == '6' and sys.argv[2] == '9'):
			plt.title(graphicsName[12])
			
		elif (sys.argv[1] == '6' and sys.argv[2] == '7'):
			plt.title(graphicsName[13])
			
	else:
		print "Combinacion de equipos y sensores desconocida"
	
else:
	print "El uso de este graficador es python graphics.py [IDGrupo] [IDSensor]"
