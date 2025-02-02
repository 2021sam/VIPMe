import RPi.GPIO as GPIO
import time

PIN = 18

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set pin 18 as an output
# GPIO.setup(PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PIN, GPIO.OUT)

print(GPIO.HIGH)
print(GPIO.LOW)

# Blink pin 18 (turn it on and off every second)
try:
    while True:
        GPIO.output(PIN, GPIO.HIGH)  # Turn pin 18 on
        time.sleep(1)                # Wait for 1 second
        GPIO.output(PIN, GPIO.LOW)   # Turn pin 18 off
        time.sleep(5)                # Wait for 1 second
        GPIO.output(PIN, 0)   # Turn pin 18 off
        time.sleep(3)

except KeyboardInterrupt:
    print("Test interrupted. Cleaning up.")
    GPIO.cleanup()  # Reset GPIO settings
