# PiTESTER

**PiTESTER** is a Raspberry Pi-based project that monitors the state of various GPIO pins, logs their status, and serves a web page to display the current status of each pin in real-time. It is designed to provide an easy way to visually monitor hardware connected to the Raspberry Pi's GPIO pins, such as switches or sensors, via a local web server.

## Features
- Monitor the state of GPIO pins (Open/Closed)
- Serve real-time pin status on a local web page
- Log pin state changes with timestamps to a log file
- Graceful server shutdown and GPIO cleanup
- Web page refreshes every 0.8 seconds to show up-to-date information

## Requirements
- **Raspberry Pi** (any model with GPIO support)
- **Python 3.x**
- **RPi.GPIO library** for controlling the GPIO pins
- **http.server** (Python standard library) for serving the web page
- Basic HTML knowledge to modify the displayed content (optional)


### Important:
Before running the script, **you must modify the `pinlist` variable** to match the GPIO pins connected to your hardware. The `pinlist` is a dictionary where the key is the name of the device or sensor, and the value is the corresponding GPIO pin number.

Example:
```python
pinlist = {
    "Pressure Switch": 14,
    "Rollout 1": 15,
    "Rollout 2": 18,
    "Rollout 3": 23,
    "High Limit": 24
}


