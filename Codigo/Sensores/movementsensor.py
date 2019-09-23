#  MBTechWorks.com 2017
#  Use an HC-SR501 PIR to detect motion (infrared)

#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import uuid
from ipcqueue import sysvmq
import struct
import socket

#Data array that is going to be packed
data = []
data.append(1)
data.append(1)
data.append(True)

#Struct needed to pack the data that says which sensor is this
sensorData = struct.Struct('BBf')

#Packing the data
packet = sensorData.pack(data[0], data[1], data[2])

#Packing Keep Alive
packetK = sensorData.pack(data[0], 0, False)

GPIO.setmode(GPIO.BOARD)            #Set GPIO to pin numbering
pir = 8                             #Assign pin 8 to PIR
GPIO.setup(pir, GPIO.IN)            #Setup GPIO pin PIR as input
print ("Sensor initializing . . .")
time.sleep(2)                       #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")

q = sysvmq.Queue(1)

try:
  currentTime = int(time.time())
  while True:
    if GPIO.input(pir) == True:      #If PIR pin goes high, motion is detected
      q.put(packet, msg_type=1)
      time.sleep(1)
      currentTime = int(time.time())
    aliveTime = int(time.time())-currentTime
    if (aliveTime > 5):
      q.put(packetK, msg_type=1)
      currentTime = int(time.time())
except KeyboardInterrupt:           #Ctrl+c
  pass                              #Do nothing, continue to finally
    
finally:
  GPIO.cleanup()                    #reset all GPIO
  print ("Program ended")
  #registro.close()
