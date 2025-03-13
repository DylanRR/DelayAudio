import pyaudio
import wave
import numpy as np
import sounddevice

# Define the audio file and device IDs
AUDIO_FILE = "test_audio.wav"
SPEAKER_1_ID = 1
SPEAKER_2_ID = 7
SAMPLE_RATE = 48000

def play_audio(device_id, volume):
    # Open the audio file
    wf = wave.open(AUDIO_FILE, 'rb')

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open a stream with the specified device
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=SAMPLE_RATE,
                    output=True,
                    output_device_index=device_id)

    # Read data from the audio file
    data = wf.readframes(1024)

    # Play the audio file with volume adjustment
    while data:
        # Convert audio data to numpy array
        audio_data = np.frombuffer(data, dtype=np.int16)
        # Adjust volume
        audio_data = (audio_data * volume).astype(np.int16)
        # Convert back to bytes
        data = audio_data.tobytes()
        # Write data to stream
        stream.write(data)
        data = wf.readframes(1024)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate PyAudio
    p.terminate()

def main():
    while True:
        # Prompt the user to select a speaker
        print("Select a speaker to play the test audio:")
        print("1. Speaker 1")
        print("2. Speaker 2")
        choice = input("Enter 1 or 2: ")

        if choice == '1':
            device_id = SPEAKER_1_ID
        elif choice == '2':
            device_id = SPEAKER_2_ID
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue
        
        play_audio(device_id, 5) # Adjust volume as needed 5 seams to be the max before distortion

if __name__ == "__main__":
    main()