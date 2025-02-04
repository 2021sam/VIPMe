import time
import board
import busio
import adafruit_vl53l0x

# Set up I2C
i2c = busio.I2C(board.SCL, board.SDA)

try:
    # Initialize sensor
    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    print("VL53L0X sensor initialized.")
    
    # Continuously read and print distance
    while True:
        distance = sensor.range  # Accessing this property starts the ranging process
        print(f"Distance: {distance} mm")
        time.sleep(1)
except Exception as e:
    print(f"Error initializing sensor: {e}")
