#!/usr/bin/python
import RPi.GPIO as GPIO
import os   # needed for system callback
import Queue
import time
import subprocess
from phue import Bridge ## https://github.com/quentinsf/qhue
 
## Connect to Hue Bridge
b = Bridge('192.168.1.199')
b.connect()
 
SWITCH1 = 17
SWITCH2 = 27
LED1 = 22
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.OUT)
 
## The Queue module provides a FIFO implementation suitable for multi-threaded programming.
eventQueue = Queue.Queue()
 
# Define function for button press
def SWITCH1(channel): eventQueue.put('SWITCH1')
def SWITCH2(channel): eventQueue.put('SWITCH2')
 
# Set the interrupt - call ledSwitch function on button press - set debounce
GPIO.add_event_detect(17, GPIO.FALLING, callback = SWITCH1, bouncetime = 250)
GPIO.add_event_detect(27, GPIO.FALLING, callback = SWITCH2, bouncetime = 250)
 
try:
        while True:
                try:
                        event = eventQueue.get(True, 0.1)
                except Queue.Empty:
                        continue
                if event == 'SWITCH1':
                        print "The SWITCH1 event is registered."
                        ## The thing to note is that the result of GPIO.input() is a boolean value.
                        ## If the input is high, it returns True and if the input is low, it returns False.
                        ## There is no middle.
                        value = GPIO.input(LED1)                        ## Read input from port
                        if value == GPIO.HIGH:                          ## If port is released
                                GPIO.output(LED1, GPIO.LOW)             ## Turn off
                                lights_list = b.get_light_objects('list')
                                for light in lights_list:
                                        light.on = False
                        else:                                           ## Else port is off
                                GPIO.output(LED1, GPIO.HIGH)            ## Turn on
                                lights_list = b.get_light_objects('list')
                                for light in lights_list:
                                        light.on = True
                                        light.brightness = 254
                if event == 'SWITCH2':
                        print "The SWITCH2 event is registered."
 
except KeyboardInterrupt:
        GPIO.cleanup()
