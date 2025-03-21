import os
import cv2
import subprocess
import re

import cv2.data

def get_serial_from_udevadm(device_path):
    """
    Retrieve the serial number of a device using udevadm.

    Args:
        device_path (str): The path to the device (e.g., '/dev/video0').

    Returns:
        str: The serial number of the device, or None if not found.
    """
    try:
        # Run the udevadm command
        result = subprocess.run(
            ['udevadm', 'info', '--query=all', f'--name={device_path}'],
            stdout=subprocess.PIPE,
            text=True
        )
        # Parse the output for ID_SERIAL_SHORT
        for line in result.stdout.splitlines():
            if "ID_SERIAL_SHORT" in line:
                return line.split('=')[1].strip()
    except Exception as e:
        print(f"Error retrieving serial number for {device_path}: {e}")
        return None
      
def get_webcam0_serial():
  return get_serial_from_udevadm("/dev/video0")

def get_webcam2_serial():
  return get_serial_from_udevadm("/dev/video2")
      
def get_cv2_index_from_serial(serial_number):
  video0_serial_lower = get_serial_from_udevadm("/dev/video0").lower()
  video2_serial_lower = get_serial_from_udevadm("/dev/video2").lower()
  serial_number = serial_number.lower()
  
  if serial_number == video0_serial_lower:
    return 0
  elif serial_number == video2_serial_lower:
    return 2

if __name__ == "__main__":
  serial1 = "89DD42EF"
  serial2 = "A55D42EF"
  
  print (f"Webcam 1 Serial: {serial1} Cv2 index: {get_cv2_index_from_serial(serial1)}")
  print (f"Webcam 2 Serial: {serial2} Cv2 index: {get_cv2_index_from_serial(serial2)}")