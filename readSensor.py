#!/usr/bin/python
import socket
import fcntl
import struct
import time
import mraa

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

#Direccion of digital signals
button.dir(mraa.DIR_IN)  
touch.dir(mraa.DIR_IN)  
led.dir(mraa.DIR_OUT)
    
#Variables config
led.write(0)
lugares = 20
messages = " "
touchState = False
buttonState = False

while True:
    buttonState = button.read();
    touchState = touch.read();

    if(buttonState == 1)
        lugares += 1

    if(touchState == 1)
        lugares -= 1

    messages = "Disponibles: " + lugares + "    "
    myLcd.write(messages)
    time.sleep(0.3)