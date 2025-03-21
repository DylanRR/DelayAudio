import os
import subprocess
import sounddevice
import pyaudio

def get_serial_from_udevadm(device_path):
    """
    Retrieve the serial number or unique identifier of a microphone using udevadm.

    Args:
        device_path (str): The path to the device (e.g., '/dev/snd/pcmC0D0c').

    Returns:
        str: The serial number or unique identifier of the device, or None if not found.
    """
    try:
        # Run the udevadm command
        result = subprocess.run(
            ['udevadm', 'info', '--query=all', f'--name={device_path}'],
            stdout=subprocess.PIPE,
            text=True
        )
        # Parse the output for ID_SERIAL_SHORT or another unique identifier
        for line in result.stdout.splitlines():
            if "ID_SERIAL_SHORT" in line:
                return line.split('=')[1].strip()
    except Exception as e:
        print(f"Error retrieving serial number for {device_path}: {e}")
        return None

def get_microphone_serial(card_index):
    """
    Retrieve the serial number of a microphone based on its ALSA card index.

    Args:
        card_index (int): The ALSA card index (e.g., 0 for 'hw:0').

    Returns:
        str: The serial number of the microphone, or None if not found.
    """
    device_path = f"/dev/snd/controlC{card_index}"
    return get_serial_from_udevadm(device_path)


def get_card_index_from_serial(serial_number):
    """
    Retrieve the ALSA card index for a microphone based on its serial number.

    Args:
        serial_number (str): The serial number to match.

    Returns:
        int: The ALSA card index of the microphone, or None if not found.
    """
    serial_number = serial_number.lower()

    for card_index in range(30):  # Adjust the range based on the number of audio devices
        serial = get_microphone_serial(card_index)
        if serial and serial.lower() == serial_number:
            return card_index

    return None
 
  
def get_device_index_from_hardware_number(hardware_number):
    """
    Retrieve the PyAudio device index for a given ALSA hardware number.

    Args:
        hardware_number (str): The ALSA hardware number (e.g., '6').

    Returns:
        int: The PyAudio device index, or None if not found.
    """
    audio = pyaudio.PyAudio()

    try:
        # Iterate through all PyAudio devices
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            device_name = info['name']

            # Check if the device name contains the hardware number (e.g., 'hw:6')
            if f"hw:{hardware_number}," in device_name:
                return i  # Return the PyAudio device index

    except Exception as e:
        print(f"Error retrieving device index: {e}")
        return None

    finally:
        audio.terminate()

    return None



if __name__ == "__main__":
    serial_number = "4B0A956FEE7B486C95038442A3087917"  # Replace with the serial number of the first microphone

    alsa_card_index = get_card_index_from_serial(serial_number)
    pyaudioIndex = get_device_index_from_hardware_number(str(alsa_card_index))

    print(f"Microphone 1 Serial: {serial_number} ALSA Card Index: {alsa_card_index} PyAudio Index: {pyaudioIndex}")