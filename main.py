import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)
GPIO.setup(14, GPIO.IN)

x=0
while x < 3:
    print("test")
    print(GPIO.input(14))
    x+=1
    time.sleep(1)
