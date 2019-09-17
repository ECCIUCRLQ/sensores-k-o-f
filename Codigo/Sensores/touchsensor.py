#import RPi.GPIO as GPIO
import time
import os
from ipcqueue import sysvmq

#sensor pin define
#buzzer = 14
touch = 26
#relay_in1 = 13
#relay_in2 = 19

#GPIO port init
def init():
         # ~ GPIO.setwarnings(False)
         # ~ GPIO.setmode(GPIO.BCM)
         #GPIO.setup(buzzer,GPIO.OUT)
         #GPIO.setup(relay_in1,GPIO.OUT)
         #GPIO.setup(relay_in2,GPIO.OUT)
         # ~ GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
         pass

#turn on relay
#def relay_on():
         #open relay channal1 ana channal2
         #GPIO.output(relay_in1,GPIO.LOW)
         #GPIO.output(relay_in2,GPIO.LOW)

#turn off relay
#def relay_off():
                  #GPIO.output(relay_in1,GPIO.HIGH)
                  #GPIO.output(relay_in2,GPIO.HIGH)


touchstatus = False
q = sysvmq.Queue(1)
#read digital touch sensor
def read_touchsensor():
         global touchstatus
         q.put(True, msg_type=1)
         # ~ if (GPIO.input(touch)==True):
            # ~ touchstatus = not touchstatus
            # ~ if touchstatus:
                # ~ print ("Ya Oscar!!")
                # ~ print ("\n")
                    # ~ #buzzer_on()
                    # ~ #relay_on()
                  
            # ~ else:
                # ~ print ("Turn off relay")
                # ~ print ("\n")
                           # ~ #buzzer_on()
                           # ~ #relay_off()
            # ~ pass
                  

#main loop
def main():
         print ("...................................................................System initializing...")
         init()
         #buzzer_off()
         #relay_off()
         print ("...................................................................Ok")
         print ("...................................................................Please touch")
         print ("\n")
         while True:
                  read_touchsensor()

if __name__ == '__main__':
         try:
                  main()
                  pass
         except KeyboardInterrupt:
                  pass
         pass
# ~ GPIO.cleanup()
