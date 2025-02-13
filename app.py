# Remember to test for fault proof by removing power & giving power.

import time
import board
import busio
import adafruit_vl53l0x
from flask import Flask, render_template, jsonify, request, redirect, url_for
import RPi.GPIO as GPIO
import logging

# Initialize the Flask app
app = Flask(__name__)

# Set up logging to file for both events and sensor readings
logging.basicConfig(filename='app.log', level=logging.DEBUG)
sensor_log_file = 'sensor.log'

# Set up I2C for VL53L0X sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = None
try:
    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    print("VL53L0X sensor initialized.")
except Exception as e:
    print(f"Error initializing VL53L0X sensor: {e}")

# GPIO setup for garage control
PIN_OUT = 18  # Adjust to your garage control pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_OUT, GPIO.OUT, initial=GPIO.HIGH)  # Output to control garage

# Variables to track state
garage_open = False
event_log = []

# Log event function
def log_event(message):
    event_log.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}")


# Log the app start time
log_event("VIPMe App started.")


# Get the current distance from the VL53L0X sensor and log it
def get_distance():
    if sensor:
        try:
            distance = sensor.range  # Returns distance in mm
            if distance is not None:
                with open(sensor_log_file, 'a') as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Distance: {distance} mm\n")
                return distance
            else:
                with open(sensor_log_file, 'a') as f:
                    f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR: Distance value is None\n")
                return None
        except Exception as e:
            with open(sensor_log_file, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {e}\n")
            return None
    return None



@app.route('/')
def index():
    # Read distance
    distance = get_distance()

    # External IP setup with different ports
    camera_1 = '98.36.237.144:91'
    camera_2 = '98.36.237.144:92'
    camera_ips = {
        1: camera_1,
        2: camera_2
    }

    # Define context with correct dictionary syntax
    context = {
        'garage_open': garage_open,
        'events': event_log,
        'distance': distance,
        'camera_ips': camera_ips
    }

    # Unpack context properly
    return render_template('index.html', **context)



@app.route('/toggle', methods=['POST'])
def toggle_garage():
    """ Toggle garage door open/close """
    global garage_open  # Ensure we're modifying the global garage_open variable
    print('Toggle Garage')

    # Toggle the GPIO state and update garage_open
    if garage_open:
        GPIO.output(PIN_OUT, GPIO.LOW)  # Close garage
        garage_open = False
        log_event("Garage closed.")
    else:
        GPIO.output(PIN_OUT, GPIO.HIGH)  # Open garage
        garage_open = True
        log_event("Garage opened.")
    
    # Redirect to toggle status page
    return redirect(url_for('toggle_page'))


@app.route('/toggle_page')
def toggle_page():
    """ Show the status of the garage door and redirect after 10 seconds """
    return render_template('toggle_page.html', garage_open=garage_open)



@app.route('/toggle-status', methods=['GET'])
def simulated_toggle_garage():
    """ Simulate toggling the garage door status (without controlling GPIO) """
    global garage_open  # Modify the global variable tracking the garage door status
    
    # Toggle the status of the garage (no GPIO control)
    garage_open = not garage_open
    
    # Return a simple JSON response with the updated status
    return jsonify({'status': 'success', 'garage_open': garage_open})





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
    return jsonify({"error": "Sensor not initialized or failed to read"}), 500

if __name__ == '__main__':
    log_event("System initialized.")
    app.run(host='0.0.0.0', port=5000, debug=True)
