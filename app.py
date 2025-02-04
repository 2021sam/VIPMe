# /home/x/apps/vipme/app.py
# pip install RPi.GPIO

from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import time
import logging


app = Flask(__name__)


# Set up logging to file
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# GPIO setup
PIN_IN = 17  # Adjust to your sensor pin
PIN_OUT = 4  # Adjust to your garage control pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_IN, GPIO.IN)  # Input from sensor
GPIO.setup(PIN_OUT, GPIO.OUT, initial=GPIO.LOW)  # Output to control garage

# Variables to track state
garage_open = False
event_log = []

# Log event function
def log_event(message):
    event_log.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")

# Check the current garage status
def update_garage_status():
    global garage_open
    sensor_value = GPIO.input(PIN_IN)
    garage_open = bool(sensor_value)
    return garage_open

@app.route('/')
def index():
    # Update garage status when the page is loaded
    update_garage_status()
    return render_template('index.html', garage_open=garage_open, events=event_log)

@app.route('/toggle', methods=['POST'])
def toggle_garage():
    """ Toggle garage door open/close """
    if garage_open:
        GPIO.output(PIN_OUT, GPIO.LOW)  # Close garage
        log_event("Garage closed.")
    else:
        GPIO.output(PIN_OUT, GPIO.HIGH)  # Open garage
        log_event("Garage opened.")
    
    update_garage_status()  # Update garage status after action
    return jsonify({"status": "success", "garage_open": garage_open})

@app.route('/log')
def log():
    """ Display the event log """
    return render_template('log.html', events=event_log)

if __name__ == '__main__':
    log_event("System initialized.")
    app.run(host='0.0.0.0', port=5000, debug=True)
