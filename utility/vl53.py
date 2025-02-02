import time
import board
import busio
import adafruit_vl53l0x

# Initialize the I2C bus (this uses the default bus)
i2c = busio.I2C(board.SCL, board.SDA)

# Create the VL53L0X sensor object
sensor = adafruit_vl53l0x.VL53L0X(i2c)

# The sensor starts ranging automatically when you read the distance
print("VL53L0X sensor initialized.")

try:
    while True:
        # Read and display the distance in mm
        distance = sensor.range  # Accessing this property starts the ranging process
        print(f"Distance: {distance} mm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProgram stopped.")
