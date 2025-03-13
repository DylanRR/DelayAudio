import pyaudio
from collections import deque
import sounddevice     #Must import to supress ALSA config errors for some weird reason


# Define delay in seconds
DELAY_DURATION = 2.5  # for example, 2 seconds

# Audio stream parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1  # 1 for mono and 2 for stereo
RATE = 48000
CHUNK = 2048  # Increase the buffer size

# Device indices based on your device list
# Headset 1
INPUT_DEVICE_INDEX_1 = 0   # Mic from Headset 1
OUTPUT_DEVICE_INDEX_1 = 9  # Speaker for Headset 1
# Headset 2
INPUT_DEVICE_INDEX_2 = 1   # Mic from Headset 2
OUTPUT_DEVICE_INDEX_2 = 10  # Speaker for Headset 2

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open input streams
input_stream_1 = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=INPUT_DEVICE_INDEX_1,
    frames_per_buffer=CHUNK
)

input_stream_2 = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    input_device_index=INPUT_DEVICE_INDEX_2,
    frames_per_buffer=CHUNK
)

# Open output streams
output_stream_1 = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    output_device_index=OUTPUT_DEVICE_INDEX_1,
    frames_per_buffer=CHUNK
)

output_stream_2 = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    output=True,
    output_device_index=OUTPUT_DEVICE_INDEX_2,
    frames_per_buffer=CHUNK
)

# Create buffers for delayed audio
buffer_1 = deque(maxlen=int(RATE / CHUNK * DELAY_DURATION))
buffer_2 = deque(maxlen=int(RATE / CHUNK * DELAY_DURATION))

try:
    while True:
        try:
            # Read data from input streams
            data1 = input_stream_1.read(CHUNK, exception_on_overflow=False)
            data2 = input_stream_2.read(CHUNK, exception_on_overflow=False)

            # Add data to buffers
            buffer_1.append(data1)
            buffer_2.append(data2)

            # Get delayed data from buffers
            if len(buffer_1) == buffer_1.maxlen:
                delayed_data1 = buffer_1.popleft()
            else:
                delayed_data1 = b'\x00' * CHUNK * 2

            if len(buffer_2) == buffer_2.maxlen:
                delayed_data2 = buffer_2.popleft()
            else:
                delayed_data2 = b'\x00' * CHUNK * 2

            # Write delayed data to output streams
            output_stream_1.write(delayed_data2)
            output_stream_2.write(delayed_data1)

        except IOError as e:
            print(f"Error: {e}")

except KeyboardInterrupt:
    pass

# When everything is done, release the capture
input_stream_1.stop_stream()
input_stream_1.close()
input_stream_2.stop_stream()
input_stream_2.close()
output_stream_1.stop_stream()
output_stream_1.close()
output_stream_2.stop_stream()
output_stream_2.close()
audio.terminate()