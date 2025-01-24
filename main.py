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
header = """
<!DOCTYPE html>
<html>
<meta http-equiv="Refresh" content=".5">
<style>
p {
  font-size: 50px;
}
</style>
<body>

<h1>PiTESTER</h1>
"""
footer = """
</body>
</html>
"""

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
    def log_message(self, format: str, *args: time.Any) -> None:
        pass

if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_server)
    thread.start_new_thread(start_server, ())
    GPIO.setmode (GPIO.BCM)
    pinlist = [14, 15]
    for pin in pinlist:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    x=0
    while True:
        f = open("web/index.html", "w")
        f.write(header)
        for pin in pinlist:
            pinstat = GPIO.input(pin)
            print(f"pin {pin}")
            f.write(f"<p> pin {pin} is {pinstat}.")
            print(pinstat)
        f.write(footer)
        f.close()
        time.sleep(.5)
