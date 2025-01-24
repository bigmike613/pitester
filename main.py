import RPi.GPIO as GPIO
import time
import http.server
import socketserver
import _thread as thread

hostname = "pitester"
port = 80
directory="web"

def start_server():
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"serving at port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

if __name__ == "__main__":

    thread.start_new_thread(start_server, ())
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
