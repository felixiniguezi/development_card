#!/usr/bin/python
import socket
import fcntl
import struct
import time
import mraa
import requests
import json

import pyupm_i2clcd as lcd

#PIN numbers
BUTTON_GPIO = 5      
TOUCH_GPIO = 6  
LED = 13   

#Initialize Gpio objects
button = mraa.Gpio(BUTTON_GPIO)  
touch = mraa.Gpio(TOUCH_GPIO)
led = mraa.Gpio(LED)

# LCD Screen configuration
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)
myLcd.clear()
myLcd.setColor(90, 90, 255)
myLcd.setCursor(0,0)

#Limit flags
MAX = 200

#Direccion of digital signals
button.dir(mraa.DIR_IN)  
touch.dir(mraa.DIR_IN)  
led.dir(mraa.DIR_OUT)
    
#Variables config
led.write(0)
lugares = None
messages = " "
touchState = False
buttonState = False
lastButtonState = False
lastTouchState = False


r = requests.get("http://10.43.51.167:5000/sections/P_Residencias")
content = json.loads(r.text)
lugares = content['capacity']

urlReserve = "http://10.43.51.167:5000/sections/P_Residencias/reserve/1"
urlFree = "http://10.43.51.167:5000/sections/P_Residencias/free/1"

while True:

    #------- Button and Touch control
    buttonState = button.read() == 1;
    touchState = touch.read() == 1;

    if(lastButtonState != buttonState):
        if(buttonState):
            r = requests.get(urlFree)
            print r.text
            content = json.loads(r.text)
            lugares = content['capacity']



    if(lastTouchState != touchState):
        if(touchState):
            r = requests.get(urlReserve)
            print r.text
            content = json.loads(r.text)
            lugares = content['capacity']



    lastTouchState = touchState
    lastButtonState = buttonState


    # ------ LCD -------
        #Red = 252, 18, 33
        #Amarillo = 229, 220, 22
        #Verde = 46, 254, 67

    green = lugares * (255/MAX)
    red = (MAX - lugares) * (255/MAX)

    print "Lugares: " + lugares + " Color " + str(red) + ", " + str(green)
    myLcd.setColor(red, green, 0)

    messages = "Disponibles: " + str(lugares) + " "
    myLcd.setCursor(0,5)
    myLcd.write("Zona A")
    myLcd.setCursor(1,0)
    myLcd.write(messages)


    # Wait
    time.sleep(0.05)
