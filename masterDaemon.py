import RPi.GPIO as GPIO; 
import time;
from picamera import PiCamera;
import facialRecognition;

# pin 7 is connected to output from the PIR motion sensor
pirPin = 7;
# Numbers GPIOs by physical location
GPIO.setmode(GPIO.BOARD);
#set the pirPin as an input
GPIO.setup(pirPin, GPIO.IN);


while True: #Loop indefinitely
  input_state = GPIO.input(pirPin) 
  if input_state == True:    
    print("Motion Detected -- ");
    time.sleep(0.3);
    user = facialRecognition.findUser();
    print user;
    if len(user) > 0:
        break;        

GPIO.cleanup(); #Clean up when exiting the program


