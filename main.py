import RPi.GPIO as GPIO
import time
GPIO.setmode (GPIO.BCM)
pinlist = [14, 15]
for pin in pinlist:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

x=0
while x < 300:
    for pin in pinlist:
        print(f"pin {pin}")
        print(GPIO.input(pin))
    x+=1
    time.sleep(.5)
