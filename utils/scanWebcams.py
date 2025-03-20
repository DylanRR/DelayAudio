import os
import subprocess
import re
import cv2

def get_video_device_info():
    """
    Get a list of video devices with their persistent USB paths and serial numbers.
    Returns:
        List of dictionaries with 'device', 'usb_path', and 'serial' keys.
    """
    devices = []
    video_devices = [f for f in os.listdir('/dev') if f.startswith('video')]

    for video in video_devices:
        device_path = f"/dev/{video}"
        try:
            # Get the USB path using v4l2-ctl
            result = subprocess.run(['v4l2-ctl', '--list-devices'], stdout=subprocess.PIPE, text=True)
            usb_path = None
            for line in result.stdout.splitlines():
                if video in line:
                    usb_path_match = re.search(r'\((.+)\)', line)
                    if usb_path_match:
                        usb_path = usb_path_match.group(1)
                        break

            # Get the serial number from lsusb
            serial = None
            if usb_path:
                lsusb_result = subprocess.run(['lsusb', '-v'], stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL)
                for lsusb_line in lsusb_result.stdout.splitlines():
                    if usb_path in lsusb_line:
                        serial_match = re.search(r'iSerial\s+\d+\s+(.+)', lsusb_line)
                        if serial_match:
                            serial = serial_match.group(1)
                            break

            devices.append({
                'device': device_path,
                'usb_path': usb_path,
                'serial': serial
            })
        except Exception as e:
            print(f"Error processing {video}: {e}")

    return devices

def find_webcam_by_serial(target_serial):
    """
    Find the OpenCV device index for a webcam with the given serial number.
    Args:
        target_serial (str): The serial number of the webcam.
    Returns:
        int: The OpenCV device index, or None if not found.
    """
    webcams = get_video_device_info()
    for webcam in webcams:
        if webcam['serial'] == target_serial:
            # Extract the OpenCV index from the /dev/videoX path
            index = int(webcam['device'].replace('/dev/video', ''))
            # Test if the device works with OpenCV
            cap = cv2.VideoCapture(index)
            if cap.isOpened():
                cap.release()
                return index
    return None

# Example usage
if __name__ == "__main__":
    serial_1 = "89DD42EF"  # Replace with the first webcam's serial number
    serial_2 = "A55D42EF"  # Replace with the second webcam's serial number

    index_1 = find_webcam_by_serial(serial_1)
    index_2 = find_webcam_by_serial(serial_2)

    if index_1 is not None:
        print(f"Webcam with serial {serial_1} is at OpenCV index {index_1}")
    else:
        print(f"Webcam with serial {serial_1} not found.")

    if index_2 is not None:
        print(f"Webcam with serial {serial_2} is at OpenCV index {index_2}")
    else:
        print(f"Webcam with serial {serial_2} not found.")