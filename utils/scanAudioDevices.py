import pyaudio
import sounddevice

audio = pyaudio.PyAudio()

# List all audio devices
for i in range(audio.get_device_count()):
    info = audio.get_device_info_by_index(i)
    #print(info['name'])
    print(f"Device {i}: {info['name']}")

audio.terminate()
