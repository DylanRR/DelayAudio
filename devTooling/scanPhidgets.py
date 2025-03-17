import subprocess
import re
import threading
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *

def list_phidgets():
    try:
        # Run the lsusb command and capture the output
        result = subprocess.run(['lsusb', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check for errors
        if result.returncode != 0:
            print(f"Error running lsusb: {result.stderr}")
            return []
        
        # Filter the output for lines containing "Phidgets Inc."
        phidget_lines = result.stdout.split('\n')
        
        # Extract and return serial numbers
        serial_numbers = []
        capture_next = False
        for line in phidget_lines:
            if 'Phidgets Inc.' in line:
                capture_next = True
            elif capture_next and 'iSerial' in line:
                match = re.search(r'iSerial\s+\d+\s+(\d+)', line)
                if match:
                    serial_numbers.append(match.group(1))
                capture_next = False
        
        return serial_numbers
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def listen_phidgets():
    serial_numbers = list_phidgets()
    if not serial_numbers:
        print("No Phidget devices found.")
        return None

    change_detected_event = threading.Event()
    detected_serial_number = [None]

    def on_state_change(self, state):
        if state:
            detected_serial_number[0] = self.getDeviceSerialNumber()
            change_detected_event.set()

    digital_inputs = []
    for serial in serial_numbers:
        for channel in range(8):
            digital_input = DigitalInput()
            digital_input.setDeviceSerialNumber(int(serial))
            digital_input.setChannel(channel)
            digital_input.setOnStateChangeHandler(on_state_change)
            digital_input.openWaitForAttachment(5000)
            digital_inputs.append(digital_input)

    try:
        print("Listening for changes on digital ports 0-7...")
        change_detected_event.wait()  # Wait until a change is detected
        return detected_serial_number[0]
    except KeyboardInterrupt:
        print("Stopping listener...")
    finally:
        for digital_input in digital_inputs:
            digital_input.close()

if __name__ == "__main__":
    serial_numbers = list_phidgets()
    if serial_numbers:
        print("Found Phidget Serial Numbers:")
        for idx, serial in enumerate(serial_numbers, start=1):
            print(f"Phidget {idx}: {serial}")
    else:
        print("No Phidget devices found.")

    serial_number = listen_phidgets()
    if serial_number:
        print(f"Change detected on Phidget with serial number: {serial_number}")
    else:
        print("No change detected on any Phidget.")