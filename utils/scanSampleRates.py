import pyaudio
import sounddevice

# Initialize PyAudio
audio = pyaudio.PyAudio()

# List all available devices
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    print(f"Device {i}: {device_info['name']}")
    for rate in [8000, 16000, 32000, 44100, 48000, 96000]:
        try:
            if audio.is_format_supported(rate,
                                         input_device=device_info['index'],
                                         input_channels=1,
                                         input_format=pyaudio.paInt16):
                print(f"  Supported sample rate: {rate}")
        except ValueError:
            pass

audio.terminate()
