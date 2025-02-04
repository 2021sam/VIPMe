import time
import board
import busio
import adafruit_vl53l0x
from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import logging

# Initialize the Flask app
app = Flask(__name__)

# Set up logging to file
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# Set up I2C for VL53L0X sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = None
try:
    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    print("VL53L0X sensor initialized.")
except Exception as e:
    print(f"Error initializing VL53L0X sensor: {e}")

# GPIO setup for garage control
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

# Get the current distance from the VL53L0X sensor
def get_distance():
    if sensor:
        return sensor.range  # Returns distance in mm
    return None

@app.route('/')
def index():
    # Update garage status and read distance
    update_garage_status()
    distance = get_distance()
    return render_template('index.html', garage_open=garage_open, events=event_log, distance=distance)

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

@app.route('/distance')
def distance():
    """ Return the current distance as JSON """
    dist = get_distance()
    if dist is not None:
        return jsonify({"distance": dist})
    return jsonify({"error": "Sensor not initialized"}), 500

if __name__ == '__main__':
    log_event("System initialized.")
    app.run(host='0.0.0.0', port=5000, debug=True)
