#  MBTechWorks.com 2017
#  Use an HC-SR501 PIR to detect motion (infrared)

#!/usr/bin/python

# ~ #import RPi.GPIO as GPIO
import time
import uuid
from ipcqueue import sysvmq
import struct
# ~ import socket

#Data array that is going to be packed
data = []
data.append(1)
data.append(1)
data.append(True)

#Struct needed to pack the data that says which sensor is this
sensorData = struct.Struct('BBf')

#Packing the data
packet = sensorData.pack(data[0], data[1], data[2])

#GPIO.setmode(GPIO.BOARD)            #Set GPIO to pin numbering
#pir = 8                             #Assign pin 8 to PIR
# ~ led = 10                            #Assign pin 10 to LED
#GPIO.setup(pir, GPIO.IN)            #Setup GPIO pin PIR as input
#GPIO.setup(led, GPIO.OUT)           #Setup GPIO pin for LED as output
#print ("Sensor initializing . . .")
# ~ time.sleep(2)                       #Give sensor time to startup
#print ("Active")
#print ("Press Ctrl+c to end program")

q = sysvmq.Queue(1)

try:
  #q.put(True, msg_type=1)
  while True:
    q.put(packet, msg_type=1)
    time.sleep(1)
   #if GPIO.input(pir) == True:      #If PIR pin goes high, motion is detected
       #time.sleep(1)
       #q.put(True, msg_type=1)

except KeyboardInterrupt:           #Ctrl+c
  pass                              #Do nothing, continue to finally
    
finally:
  # ~ GPIO.output(led, False)           #Turn off LED in case left on
  # ~ GPIO.cleanup()                    #reset all GPIO
  # ~ registro.close()
	print ("Program ended")
