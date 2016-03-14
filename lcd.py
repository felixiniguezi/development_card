import socket
import fcntl
import struct

import pyupm_i2clcd as lcd

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Clear
myLcd.clear()

# Green
myLcd.setColor(90, 90, 255)

# Zero the cursor
myLcd.setCursor(0,0)
lugares = 0

while (True):
	myLcd.write("Lugares disponbles: " + str(lugares))
	lugares += 1