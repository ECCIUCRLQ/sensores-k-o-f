
#  MBTechWorks.com 2017
#  Use an HC-SR501 PIR to detect motion (infrared)

#!/usr/bin/python

#import RPi.GPIO as GPIO
import time
import uuid
from ipcqueue import sysvmq
# ~ import socket

# ~ HOST = '10.1.138.111'  # The server's hostname or IP address
# ~ PORT = 5000        # The port used by the server

#GPIO.setmode(GPIO.BOARD)            #Set GPIO to pin numbering
# ~ pir = 8                             #Assign pin 8 to PIR
# ~ led = 10                            #Assign pin 10 to LED
# ~ GPIO.setup(pir, GPIO.IN)            #Setup GPIO pin PIR as input
# ~ GPIO.setup(led, GPIO.OUT)           #Setup GPIO pin for LED as output
# ~ print ("Sensor initializing . . .")
# ~ time.sleep(2)                       #Give sensor time to startup
# ~ print ("Active")
# ~ print ("Press Ctrl+c to end program")
# ~ avance = 0
q = sysvmq.Queue(1)
#q.size()
# ~ from uuid import getnode as get_mac
# ~ mac = get_mac()
# ~ mensaje = "Movement detected by Raspberry KOF " + str(mac)
# ~ registro = open('reporte.txt', 'w')
try:
  q.put(True, msg_type=1)
  while True:
   if GPIO.input(pir) == True:      #If PIR pin goes high, motion is detected
       # ~ time.sleep(1)
       # ~ print (mensaje + str(avance))
       # ~ registro.write(mensaje + time.strftime("%c") +"\n")
       # ~ avance = avance + 1
       q.put(True, msg_type=1)
       
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     #s.connect((HOST, PORT))
     #s.sendall(b'KOF: The King of Fighters\n')
     #data = s.recv(1024)  

except KeyboardInterrupt:           #Ctrl+c
  pass                              #Do nothing, continue to finally
    
finally:
  # ~ GPIO.output(led, False)           #Turn off LED in case left on
  # ~ GPIO.cleanup()                    #reset all GPIO
  # ~ registro.close()
  print ("Program ended")
    
