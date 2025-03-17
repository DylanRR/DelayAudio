import pyaudio
import sounddevice
import numpy as np

def list_audio_devices():
    audio = pyaudio.PyAudio()
    devices = []

    # List all audio devices
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        devices.append(info['name'])

    audio.terminate()
    return devices


def play_test_tone(device_index, sample_rate= 48000, duration=1.0, volume=0.5):
    try: 
        fs = sample_rate  # Sample rate
        p = pyaudio.PyAudio()

        # Generate a 440 Hz tone
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        tone = (volume * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

        # Open a stream with the specified device
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=fs,
                        output=True,
                        output_device_index=device_index)

        # Play the tone
        stream.write(tone.tobytes())
    except Exception as e:
        print(f"Error playing test tone: {e}")
        return False
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

"""
if __name__ == "__main__":
    devices = list_audio_devices()
    for idx, device in enumerate(devices):
        print(f"Device {idx}: {device}")"
#"""