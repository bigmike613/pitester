import RPi.GPIO as GPIO
import time
import http.server
import socketserver

hostname = "pitester"
port = 80
Handler = http.server.SimpleHTTPRequestHandler

if __name__ == "__main__":
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"serving at port {port}")
        httpd.serve_forever()
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
