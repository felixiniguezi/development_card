#!/usr/bin/python
import mraa     # For accessing the GPIO
import time     # For sleeping between blinks

BUTTON_GPIO = 5                   # we are using D5 pin
button = mraa.Gpio(BUTTON_GPIO)  # Get the LED pin object
button.dir(mraa.DIR_IN)     # Set the direction as output

led = mraa.Gpio(13)   
led.dir(mraa.DIR_OUT)        
led.write(0)

# One infinite loop coming up
while True:
    if button.read() == 1:
        # LED is off, turn it on
        led.write(1)

    else:
        led.write(0)

    time.sleep(1)