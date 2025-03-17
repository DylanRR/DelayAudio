import pyaudio
import sounddevice


def list_supported_sample_rates():
    try:
        audio = pyaudio.PyAudio()
        devices = []

        # List all available devices and their supported sample rates
        for i in range(audio.get_device_count()):
            device_info = audio.get_device_info_by_index(i)
            supported_rates = []
            for rate in [8000, 16000, 32000, 44100, 48000, 96000]:
                try:
                    if audio.is_format_supported(rate,
                                                input_device=device_info['index'],
                                                input_channels=1,
                                                input_format=pyaudio.paInt16):
                        supported_rates.append(rate)
                except ValueError:
                    pass
                except Exception as e:
                    print(f"Skipping device {i} due to error: {e}")
                    break  # Skip this device if any other exception occurs
            else:
                devices.append({
                    'device_number': i,
                    'device_info': device_info,
                    'supported_sample_rates': supported_rates
                })

        audio.terminate()
        return devices
    except Exception as e:
        pass

if __name__ == "__main__":
    devices = list_supported_sample_rates()
    for device in devices:
        print(f"Device {device['device_number']}: {device['device_info']['name']}")
        print(f"  Supported sample rates: {device['supported_sample_rates']}")