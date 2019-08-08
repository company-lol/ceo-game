import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time 
import led

led.clear()
led.display("1")

led.clear()


x = range(999999)
x.reverse()

for i in x:
    led.display(str(i))
