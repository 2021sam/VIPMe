import time
import board
import busio
import adafruit_vl53l0x

def main():
    # Create I2C bus and sensor object
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_vl53l0x.VL53L0X(i2c)

    # Start the sensor
    sensor.start_ranging()

    print("VL53L0X sensor initialized.")

    try:
        while True:
            # Read and display the distance in mm
            distance = sensor.range
            print(f"Distance: {distance} mm")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nProgram stopped.")
    
    finally:
        # Stop the sensor when finished
        sensor.stop_ranging()

if __name__ == "__main__":
    main()
