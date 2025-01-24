import RPi.GPIO as GPIO
import time
import datetime
import http.server
import socketserver
import _thread as thread
import signal
import sys

# Edit this list to add or remove pins to be monitored (using GPIO pin numbers)
pinlist = {"Pressure Switch":14, "Rollout 1":15, "Rollout 2":18, "Rollout 3":23, "High Limit":24}

# Function to create a working list from the pinlist. This prepares a list of pins to monitor.
def createworkinglist(startlist):
    global workinglist
    # Iterate through the pinlist and create a new entry for each pin in the workinglist
    for name, num in startlist.items():
        workinglist.append({"name":name, "num":num, "pre_status":None, "status":None})

# Global list to store information about each pin
workinglist = []
# Port and directory for the web server
port = 80
directory="web"
# global var initilization
httpd = None
# HTML template for the web page header, includes a refresh to update every 0.8 seconds
header = """
<!DOCTYPE html>
<html>
<meta http-equiv="Refresh" content=".8">
<style>
p {
  font-size: 50px;
}
table, th, td {
  border:1px solid black;
}
#red {
background-color: red;
}
#green{
background-color: green;
}
</style>
<body>

<h1 align=center>PiTESTER</h1>
<table style="width:100%">
<tr>
<th>Name</th>
<th>Pin</th>
<th>Status</th>
</tr>
"""
# HTML footer template for closing the table and body
footer = """
</table>
</body>
</html>
"""
# Function to start the HTTP server to serve the web page
def start_server():

    global httpd
    # Set up the server to listen on the specified port and handle HTTP requests using the Handler class
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"serving at port {port}")
        httpd.serve_forever()

# Signal handler to stop the server when the user interrupts the program (Ctrl+C)
def stop_server(signal, frame):
    global httpd
    print("Stopping the server...")
    if httpd:
        httpd.shutdown() # Shutdown the HTTP server gracefully
    # Add ending statement to log file
    fl = open("/home/mike/pitest.log", "a")
    now = datetime.datetime.now()
    fl.write(f"\n")
    fl.write(f"{now} - Application Stopped\n")
    fl.write(f"\n")
    fl.close()
    GPIO.cleanup() # Cleanup the GPIO setup before exiting
    sys.exit(0) # Exit the program

# Custom HTTP request handler to serve the web page (stops default log messages)
class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)
    def log_message(self, format, *args) -> None:
        pass # Override to prevent default logging

# Main program execution starts here
if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_server)  # Handle SIGINT (Ctrl+C) to stop the server
    thread.start_new_thread(start_server, ())  # Start the HTTP server in a new thread
    GPIO.setmode (GPIO.BCM) # Set the GPIO pin numbering mode to BCM (Broadcom)
    createworkinglist(pinlist) # Initialize the working list from the pinlist

    # Set up each pin in the pinlist as an input with a pull-up resistor
    for pin in pinlist.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Log the start of the application
    fl = open("/home/mike/pitest.log", "a")
    now = datetime.datetime.now()
    fl.write(f"\n")
    fl.write(f"{now} - Application Started\n")
    fl.write(f"\n")
    fl.close()

    # Main loop to update the web page and monitor GPIO pins
    while True:
        # Open the web page index.html for writing the status
        f = open("web/iframe.html", "w")
        fl = open("/home/mike/pitest.log", "a")
        f.write(header)

        # Iterate over the working list to check the status of each pin
        for pin in workinglist:
            pinstat = GPIO.input(pin['num']) # Read the current state of the GPIO pin
            fl.write(f"")

            # Update the web page with the pin's status (Open or Closed)
            if pinstat:
                # Pin is "Open" (not connected to ground)
                f.write(f"<tr id=red><td>")
                f.write(f"{pin['name']}</td><td>{pin['num']}</td><td>Open</td></tr>")
                pin['status']=1 # Update status to 1 (Open)
            else:
                # Pin is "Closed" (connected to ground)
                f.write(f"<tr id=green><td>")
                f.write(f"{pin['name']}</td><td>{pin['num']}</td><td>Closed</td></tr>")
                pin['status']=0 # Update status to 0 (Closed)
            
            # Check if the pin's status has changed compared to the previous state
            if pin['pre_status'] != None:
                if pin['pre_status'] != pin['status']:
                    now = datetime.datetime.now()
                    fl.write(f"{now} - {pin['name']} on pin {pin['num']} changed state from {pin['pre_status']} to {pin['status']}\n")
            # Update the previous state for the next loop
            pin['pre_status']=pinstat

        # Write the HTML footer and close the file
        f.write(footer)
        f.close()
        fl.close()

        # Sleep for a short period before checking the pins again
        time.sleep(.1)
