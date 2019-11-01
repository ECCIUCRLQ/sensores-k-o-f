import RPi.GPIO as GPIO
from time import time
import time
import os
from ipcqueue import sysvmq
import struct

touch = 12

#Data array that is going to be packed
data = []
data.append(5)
data.append(1)
data.append(True)



#Struct needed to pack the data that says which sensor is this
sensorData = struct.Struct('BBf')

#Packing the data
packet = sensorData.pack(data[0], data[1], data[2])

#Packing Keep Alive
packetK = sensorData.pack(data[0], 0, False)
#GPIO port init
def init():
         GPIO.setwarnings(False)
         GPIO.setmode(GPIO.BOARD)
         GPIO.setup(touch,GPIO.IN)
         pass
         
touchstatus = False
q = sysvmq.Queue(1)
#read digital touch sensor
def read_touchsensor():
         global touchstatus
         if (GPIO.input(touch)==True):
            touchstatus = not touchstatus
            if touchstatus:
               q.put(packet, msg_type=1)
               #print("Touched")
               keepAlive = True
               time.sleep(1)
            # ~ else:
                # ~ print ("Turn off relay")
                # ~ print ("\n")
            # ~ pass

#main loop
def main():
         time.sleep(1)
         print ("...................................................................System initializing...")
         init()
         print ("...................................................................Ok")
         print ("...................................................................Please touch")
         print ("\n")
         #Keep Alive
         keepAlive = False
         currentTime = int(time.time())
         while True:
            if (keepAlive == False):
               aliveTime = int(time.time())-currentTime
               if(aliveTime > 5):
                  q.put(packetK, msg_type=1)
                  currentTime = int(time.time())
                  keepAlive = True
            if keepAlive == True:
               currentTime = int(time.time())
               keepAlive = False
            read_touchsensor()

if __name__ == '__main__':
         try:
                  main()
                  pass
         except KeyboardInterrupt:
                  pass
         pass
	#GPIO.cleanup()
