from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
import time

class phidgetController:
  def __init__(self, serial_number, channels):
    self.serial_number = serial_number
    self.channels = channels
    self.digital_inputs = {}

  def init(self):
    try:
      for channel in self.channels:
        digital_input = DigitalInput()
        digital_input.setDeviceSerialNumber(self.serial_number)
        digital_input.setChannel(channel)
        digital_input.openWaitForAttachment(5000)
        self.digital_inputs[channel] = digital_input
      return True
    except PhidgetException as e:
      print(f"Error initializing Phidget: {e}")
      return False

  def is_button_pressed(self, channel):
    if channel in self.digital_inputs:
      return self.digital_inputs[channel].getState()
    else:
      print(f"Channel {channel} not initialized.")
      return False

  def close(self):
    for digital_input in self.digital_inputs.values():
      digital_input.close()
    print (f"Phidget {self.serial_number} controller closed.")

# Example usage
"""
if __name__ == "__main__":
  phidget = phidgetController(serial_number=678328, channels=[0, 1])
  phidget2 = phidgetController(serial_number=678505, channels=[0, 1])
  if phidget.init():
    print("Phidget initialized successfully.")
    if phidget2.init():
      print("Phidget 2 initialized successfully.")
      while True:
        print (f"Phidget 1 - Channel 0: {phidget.is_button_pressed(0)}")
        print (f"Phidget 1 - Channel 1: {phidget.is_button_pressed(1)}")
        print (f"Phidget 2 - Channel 0: {phidget2.is_button_pressed(0)}")
        print (f"Phidget 2 - Channel 1: {phidget2.is_button_pressed(1)}")
        time.sleep(1)
    else:
      print("Failed to initialize Phidget 2.")
  else:
    print("Failed to initialize Phidget 1.")
#"""