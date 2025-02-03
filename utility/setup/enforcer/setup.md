# Seco-Larm E-931-S35RRQ with Raspberry Pi

## Overview

The **Seco-Larm E-931-S35RRQ** is a reflective photoelectric beam sensor that can be used for detecting motion, object presence, or security applications. This guide explains how to connect the sensor to a **Raspberry Pi** and read its output using Python.

## Features

- **Reflective infrared beam** for motion detection
- **Relay output (NO/NC)** for easy integration
- **12-30VDC power input**
- **Adjustable sensing range** (up to 22 inches)

## Wiring

### **Sensor Wire Functions**

| Wire Color | Function                           |
| ---------- | ---------------------------------- |
| **Blue**   | Power (+12-30VDC)                  |
| **Green**  | Ground (GND)                       |
| **White**  | Normally Open (NO) Relay Contact   |
| **Black**  | Normally Closed (NC) Relay Contact |
| **Brown**  | Common (COM) Relay Contact         |

### **Connecting to Raspberry Pi**

1. **Power the sensor** (Use an external **12VDC** power supply):
   - **Blue** → **+12VDC**
   - **Green** → **GND (of power supply & Raspberry Pi)**
2. **Connect the relay output to Raspberry Pi GPIO**:
   - **Brown (COM)** → **Raspberry Pi GND**
   - **White (NO) or Black (NC)** → **GPIO17 (Pin 11) on Raspberry Pi**
   - (Recommended: Use NO so that the signal triggers when the beam is interrupted)

## Python Script

Install the **RPi.GPIO** library (if not installed):

```bash
sudo apt update
sudo apt install python3-rpi.gpio
```

Run the following Python script to detect beam interruptions:

```python
import RPi.GPIO as GPIO
import time

SENSOR_PIN = 17  # Change this if using a different GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Internal pull-up resistor

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:  # Relay closed (beam broken)
            print("Beam Broken!")
        else:
            print("Beam Clear")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
```

## How It Works

- **Beam Clear (NO open, NC closed)** → GPIO reads **HIGH (1)**
- **Beam Broken (NO closed, NC open)** → GPIO reads **LOW (0)**
- The script detects state changes and prints the result.

## Customization

- **Use GPIO pin 17** (modify `SENSOR_PIN` for a different pin).
- **Change NO/NC logic** by using the **Black (NC)** wire instead of White (NO).
- **Integrate with alarms, cameras, or notifications** using the detected signal.

## Troubleshooting

- **No signal changes?** Check power wiring and confirm the LED indicators work.
- **False triggers?** Use an **optocoupler** or debounce the input in software.
- **No 5V output?** The relay is a **switch**, not a voltage source. Pull-up resistors are used for detection.

## Next Steps

- Integrate with **Home Assistant**, **Node-RED**, or other automation systems.
- Connect multiple sensors for **security zones** or **motion detection**.
- Use with a **buzzer** or **camera module** for alerts.

---

**Author:** Your Name\
**Last Updated:** YYYY-MM-DD