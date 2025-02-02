Ah, got it! It seems like the **relay's behavior is active-high** for the **control pin (IN)**, and it behaves inversely with respect to the green LED:

- When **GPIO is HIGH (3.3V)**, the relay is **off**, and the **green LED is off**.
- When **GPIO is LOW (0V)**, the relay is **on**, and the **green LED is on**.

This is the opposite of what we initially thought (active-low). In this case, the relay is **active-high**, meaning it gets triggered when the GPIO pin is **LOW**, and it deactivates when the GPIO pin is **HIGH**.

Thanks for clarifying this! Here's how you can update the **README** with this behavior:

---

# Raspberry Pi Relay Setup: Tongling JQC-31-F-S-Z

This guide walks you through setting up a **Tongling JQC-31-F-S-Z** 5V relay with your **Raspberry Pi** and controlling it through the GPIO pins.

---

## 1. Wiring the Relay to the Raspberry Pi

### **Step 1: Relay Module Pinout**
The **JQC-31-F-S-Z** relay module has 3 pins:
- **VCC**: Connects to the **5V** supply (either from the Raspberry Pi’s 5V pin or an external 5V source).
- **GND**: Connects to **Ground (GND)**.
- **IN**: The control pin that connects to a **GPIO pin** on the Raspberry Pi.

### **Step 2: Raspberry Pi GPIO Pin Setup**
- **VCC** → **5V Pin** on Raspberry Pi (Pin 2 or Pin 4)
- **GND** → **Ground Pin** on Raspberry Pi (Pin 6)
- **IN** → **GPIO Pin** (e.g., GPIO 18, Pin 12 on the Raspberry Pi)

If you're powering the relay from an **external 5V power source**, make sure to connect the **ground** of the power supply to the **ground** of the Raspberry Pi.

---

## 2. Relay Behavior

The relay’s **green LED** will behave as follows:
- When the **GPIO Pin is HIGH (3.3V)**, the relay is **OFF**, and the **green LED is OFF**.
- When the **GPIO Pin is LOW (0V)**, the relay is **ON**, and the **green LED is ON**.

This means the relay is **active-high**, and it gets triggered when the GPIO pin is set to **LOW**.

---

## 3. Python Code to Control the Relay

You can use the **RPi.GPIO** library to control the relay through Python.

### **Step 1: Install RPi.GPIO Library**
First, ensure you have the **RPi.GPIO** library installed. It’s usually pre-installed with Raspberry Pi OS, but if not, install it via:

```bash
sudo apt-get update
sudo apt-get install python3-rpi.gpio
```

### **Step 2: Python Script to Control the Relay**

Here’s a basic Python script to turn the relay on and off:

```python
import RPi.GPIO as GPIO
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)

# Set GPIO pin 18 as an output
GPIO.setup(18, GPIO.OUT)

# Turn relay ON (GPIO LOW)
GPIO.output(18, GPIO.LOW)  # This will trigger the relay (green LED ON)
time.sleep(1)

# Turn relay OFF (GPIO HIGH)
GPIO.output(18, GPIO.HIGH)  # This will deactivate the relay (green LED OFF)
time.sleep(1)

# Clean up GPIO settings
GPIO.cleanup()
```

### **Step 3: Running the Script**
1. Save the script as `relay_control.py`.
2. Run the script with:

```bash
python3 relay_control.py
```

---

## 4. Troubleshooting

### **Relay Not Triggering (When VDC is 3.3V)**

If the relay isn't triggering correctly:
- **Check your wiring**: Ensure the **VCC**, **GND**, and **IN** pins are connected correctly.
- **Test your relay's behavior**: If you're using the **3.3V GPIO pin**, make sure it's sufficient to trigger the relay. If not, use a **transistor** or **MOSFET** to switch the relay.

### **Transistor Circuit Setup**:
If your relay isn’t triggering reliably with the 3.3V GPIO signal, use an **NPN transistor** (e.g., **2N2222**) as a switch:

- **GPIO Pin (Pin 18)** → **Base of NPN transistor** (with a 1kΩ resistor).
- **Emitter of transistor** → **Ground**.
- **Collector of transistor** → **IN Pin of the Relay**.
- **Relay's VCC** → **External 5V power supply**.

---

## 5. Final Thoughts

- The **Tongling JQC-31-F-S-Z** relay module is a great option for controlling high-power devices with the Raspberry Pi.
- **Active-high logic**: The relay turns on when the GPIO pin is **LOW**, and turns off when the GPIO pin is **HIGH**.
- If your relay isn't triggering reliably with 3.3V, consider using a **transistor or MOSFET** to provide more current and proper voltage.

---

## 6. Additional Resources
- [RPi.GPIO Documentation](https://pypi.org/project/RPi.GPIO/)
- [Tongling JQC-31-F-S-Z Relay Datasheet](https://www.poningroup.com/download/JQC-31-F.pdf)

---

Let me know if you need any further clarifications or additional changes to the guide!