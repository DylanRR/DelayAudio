import pyudev

# Initialize the context for pyudev
context = pyudev.Context()

def get_hardware_id(serial_number):
    # Iterate over all USB devices
    for device in context.list_devices(subsystem='usb'):
        # Check if the device has a serial number and compare it
        if device.get('ID_SERIAL') == serial_number:
            # Return the hardware ID (could be the device's ID or other identifying info)
            return device.get('ID_USB_DRIVER'), device.get('ID_MODEL_ID'), device.get('ID_VENDOR_ID')
    return None

# Replace 'YOUR_SERIAL_NUMBER' with the USB serial number you're looking for
serial_number = 'MVX2U#2-b71cdcfb0cbedc549200ce724ab01ba6'
serial_number2 = 'MVX2U#2-b024f7fd59cb675ab7b3afcfe2015bed'

hardware_id = get_hardware_id(serial_number)
if hardware_id:
    print(f"Hardware ID for Serial Number {serial_number}:")
    print(f"  USB Driver: {hardware_id[0]}")
    print(f"  Model ID: {hardware_id[1]}")
    print(f"  Vendor ID: {hardware_id[2]}")
else:
    print(f"No device found with serial number {serial_number}")
