#!/usr/bin/python
import socket
import fcntl
import struct
import time
import mraa
import requests

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

RedFlag = 0
YellowFlag = 10

#Direccion of digital signals
button.dir(mraa.DIR_IN)  
touch.dir(mraa.DIR_IN)  
led.dir(mraa.DIR_OUT)
    
#Variables config
led.write(0)
lugares = 5
messages = " "
touchState = False
buttonState = False
lastButtonState = False
lastTouchState = False


urlReserve = "http://10.43.51.167:5000/sections/1/reserve/1"
urlFree = "http://10.43.51.167:5000/sections/1/free/1"

while True:

    #------- Button and Touch control
    buttonState = button.read() == 1;
    touchState = touch.read() == 1;

    if(lastButtonState != buttonState):
        if(buttonState):
            lugares += 1
            r = requests.get(urlReserve)
            print r.status_code
            print r.headers
            print r.encoding
            print r.text

    if(lastTouchState != touchState):
        if(touchState):
            lugares -= 1
            r = requests.get(urlFree)
            print r.status_code
            print r.headers
            print r.encoding
            print r.text


    lastTouchState = touchState
    lastButtonState = buttonState


    # ------ LCD -------
        #Red = 252, 18, 33
        #Amarillo = 229, 220, 22
        #Verde = 46, 254, 67

    if(lugares <= RedFlag):
        myLcd.setColor(252, 18, 3)

    elif(lugares <= YellowFlag):
        myLcd.setColor(229, 220, 22)

    else:
        myLcd.setColor(46, 254, 67)

    messages = "Disponibles: " + str(lugares) + " "
    myLcd.setCursor(0,0)
    myLcd.write(messages)


    # Wait
    time.sleep(0.1)