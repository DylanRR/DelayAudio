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


def get_pyaudio_index_from_serial(serial_number):
    """
    Retrieve the PyAudio device index for a microphone based on its serial number.

    Args:
        serial_number (str): The serial number of the microphone.

    Returns:
        int: The PyAudio device index, or None if not found.
    """
    alsa_card_index = get_card_index_from_serial(serial_number)
    if alsa_card_index is not None:
        return int(get_device_index_from_hardware_number(int(alsa_card_index)))
    else:
        print(f"No device found with serial number {serial_number}")
    return None

def get_device_index_from_name(name):
    """
    Retrieve the PyAudio device index for a given name.
    Matches if the passed-in name is contained in the device name (case insensitive).

    Args:
        name (str): The partial or full name of a device (e.g., 'KT USB Audio').

    Returns:
        int: The PyAudio device index, or None if not found.
    """
    audio = pyaudio.PyAudio()
    try:
        # Iterate through all PyAudio devices
        for i in range(audio.get_device_count()):
            info = audio.get_device_info_by_index(i)
            device_name = info['name'].lower()

            # Check if the passed-in name is contained in the device name (case insensitive)
            if name.lower() in device_name:
                return i  # Return the PyAudio device index

    except Exception as e:
        print(f"Error retrieving device index: {e}")
        return None

    finally:
        audio.terminate()


if __name__ == "__main__":
    serial_number1 = 'MVX2U#2-b71cdcfb0cbedc549200ce724ab01ba6'
    serial_number2 = 'MVX2U#2-b024f7fd59cb675ab7b3afcfe2015bed'
    
    name1 = 'KT USB Audio: - (hw:1,0)' #This is just for testing we would not want to include the HW number in the name as it could change
    name2 = 'KT USB Audio: - (hw:3,0)'

    print(f"Microphone 1 Serial: {serial_number1} PyAudio Index: {get_pyaudio_index_from_serial(serial_number1)}")
    print(f"Microphone 2 Serial: {serial_number2} PyAudio Index: {get_pyaudio_index_from_serial(serial_number2)}")
    print(f"Speaker 1 Name: {name1} PyAudio Index: {get_device_index_from_name(name1)}")
    print(f"Speaker 2 Name: {name2} PyAudio Index: {get_device_index_from_name(name2)}")