import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)
GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

x=0
while x < 300:
    print("test")
    print(GPIO.input(14))
    x+=1
    time.sleep(1)
