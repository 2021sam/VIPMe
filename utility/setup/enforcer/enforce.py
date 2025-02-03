import RPi.GPIO as GPIO
import time

SENSOR_PIN = 17  # Change to the GPIO pin you connected to

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable internal pull-up resistor

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:  # Relay closed (beam interrupted)
            print("Beam Broken!")
        else:
            print("Beam Clear")
        time.sleep(0.5)  # Adjust for real-time needs
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()