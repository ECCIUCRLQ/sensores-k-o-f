#!/bin/bash 
python2 server.py &
sleep 1
python2 client.py &
sleep 1
python2 interpreter.py &
sleep 1
cd ..
cd Sensores/
python2 movementsensor.py &
python2 touchsensor.py &
