import time
import uuid
from ipcqueue import sysvmq
import struct
import socket
from random import randrange

#Data array that is going to be packed
data = []
data.append(1) #Sensor Id
data.append(1) #Data type
data.append(True) #Data

#Struct needed to pack the data that says which sensor is this
sensorData = struct.Struct('BBf')

#Packing the data
packet = sensorData.pack(data[0], data[1], data[2])

#Packing Keep Alive
packetK = sensorData.pack(data[0], 0, False)

print ("Sensor initializing . . .")
time.sleep(2)                       #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")

q = sysvmq.Queue(1)

try:
  currentTime = int(time.time())
  while True:
    input = int(randrange(1)) 
    time.sleep(1)
    if input == 1:      #If PIR pin goes high, motion is detected
      q.put(packet, msg_type=1)
      time.sleep(1)
      currentTime = int(time.time())
    aliveTime = int(time.time())-currentTime
    if (aliveTime > 5):
      q.put(packetK, msg_type=1)
      currentTime = int(time.time())
except KeyboardInterrupt:           #Ctrl+c
  pass                              #Do nothing, continue to finally
    
finally:                    #reset all GPIO
  print ("Program ended")
  #registro.close()
