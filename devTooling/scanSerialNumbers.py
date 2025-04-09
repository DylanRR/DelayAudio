import subprocess
import re

def get_usb_devices():
    try:
        # Run the lsusb -v command
        result = subprocess.run(['lsusb', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Error running lsusb:", result.stderr)
            return []

        devices = result.stdout.split('\n\n')  # Split output into blocks for each device
        device_list = []
        for device in devices:
            if not device.strip():
                continue

            # Extract device name (using the "iProduct" field)
            name_match = re.search(r'^\s*iProduct\s+\d+\s+(.*)', device, re.MULTILINE)
            device_name = name_match.group(1).strip() if name_match else "Unknown Device"

            # Extract serial number (using the "iSerial" field)
            serial_match = re.search(r'^\s*iSerial\s+\d+\s+(.*)', device, re.MULTILINE)
            serial_number = serial_match.group(1).strip() if serial_match else "No Serial Number"

            # Filter out invalid serial numbers, host controllers, and Bluetooth radios
            if (
                serial_number == "No Serial Number" or
                re.match(r'^\s*bNumConfigurations', serial_number) or
                "Host Controller" in device_name or
                "Bluetooth" in device_name
            ):
                continue

            device_list.append((device_name, serial_number))

        return device_list

    except FileNotFoundError:
        print("Error: lsusb command not found. Please ensure it is installed.")
        return []


def get_webcam_devices():
    try:
        # Run the lsusb -v command
        result = subprocess.run(['lsusb', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print("Error running lsusb:", result.stderr)
            return []

        devices = result.stdout.split('\n\n')  # Split output into blocks for each device
        device_list = []
        for device in devices:
            if not device.strip():
                continue

            # Extract device name (using the "iProduct" field)
            name_match = re.search(r'^\s*iProduct\s+\d+\s+(.*)', device, re.MULTILINE)
            device_name = name_match.group(1).strip() if name_match else "Unknown Device"

            # Extract serial number (using the "iSerial" field)
            serial_match = re.search(r'^\s*iSerial\s+\d+\s+(.*)', device, re.MULTILINE)
            serial_number = serial_match.group(1).strip() if serial_match else "No Serial Number"

            # Filter out non-webcam devices
            if "webcam" not in device_name.lower():
                continue

            device_list.append((device_name, serial_number))

        return device_list

    except FileNotFoundError:
        print("Error: lsusb command not found. Please ensure it is installed.")
        return []


"""
# Example usage:

if __name__ == "__main__":
    # USB devices
    devices = get_usb_devices()
    if devices:
        print("USB Devices:")
        for device_name, serial_number in devices:
            print(f"Device: {device_name}, Serial Number: {serial_number}")
    else:
        print("No USB devices found.")

    print("\n")

    # Webcam devices
    webcam_devices = get_webcam_devices()
    if webcam_devices:
        print("Webcam Devices:")
        for device_name, serial_number in webcam_devices:
            print(f"Device: {device_name}, Serial Number: {serial_number}")
    else:
        print("No Webcam devices found.")
"""