from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
import time

# Replace these with your actual device serial numbers
PHIDGET_SERIAL_NUMBERS = [678328, 678505]

# Declare any event handlers here. These will be called every time the associated event occurs.
def onStateChange(self, state):
    print(f"State [Serial: {self.getDeviceSerialNumber()}, Channel: {self.getChannel()}]: {'Pressed' if state else 'Released'}")

def main():
    # Create a list to hold the DigitalInput objects
    digitalInputs = []

    # Create DigitalInput objects for each button on both Phidget Interface Kits
    for serial_number in PHIDGET_SERIAL_NUMBERS:
        for channel in range(2):  # Each Phidget has 2 buttons (D0 and D1)
            digitalInput = DigitalInput()
            digitalInput.setDeviceSerialNumber(serial_number)
            digitalInput.setChannel(channel)
            digitalInput.setOnStateChangeHandler(onStateChange)
            digitalInputs.append(digitalInput)

    # Open your Phidgets and wait for attachment
    try:
        for digitalInput in digitalInputs:
            digitalInput.openWaitForAttachment(10000)  # Increased timeout to 10 seconds
    except PhidgetException as e:
        print(f"PhidgetException {e.code} ({e.details})")
        return

    # Do stuff with your Phidgets here or in your event handlers.
    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

    # Close your Phidgets once the program is done.
    for digitalInput in digitalInputs:
        digitalInput.close()

if __name__ == "__main__":
    main()