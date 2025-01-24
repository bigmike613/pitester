import RPi.GPIO as GPIO
import time
import http.server
import socketserver
import _thread as thread
import signal
import sys

port = 80
directory="web"
httpd = None

def start_server():
    global httpd
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"serving at port {port}")
        httpd.serve_forever()

def stop_server(signal, frame):
    global httpd
    print("Stopping the server...")
    if httpd:
        httpd.shutdown()
    GPIO.cleanup()
    sys.exit(0)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_server)
    thread.start_new_thread(start_server, ())
    GPIO.setmode (GPIO.BCM)
    pinlist = [14, 15]
    for pin in pinlist:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    x=0
    while x < 300:
        f = open("web/index.html", "w")
        f.write("TESTING123...")
        for pin in pinlist:
            print(f"pin {pin}")
            print(GPIO.input(pin))
        f.close()
        x+=1
        time.sleep(.5)
