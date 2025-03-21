import time
import numpy as np
import sounddevice as sd
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *
from videoController import videoController
import threading
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import configuration_loader_v2 as configuration_loader
from config import advancedAudioScan as AAS
from config import advancedWebcamScan as AWS

config_path = configuration_loader.get_config_path()
CL = configuration_loader.ConfigurationLoader(config_path)

# Configurable Variables

MIC_INDEX_1 = AAS.get_pyaudio_index_from_serial('MVX2U#2-b71cdcfb0cbedc549200ce724ab01ba6')
MIC_INDEX_2 = AAS.get_pyaudio_index_from_serial('MVX2U#2-b71cdcfb0cbedc549200ce724ab01ba6')

SPEAKER1_INDEX = AAS.get_device_index_from_name('KT USB Audio')
SPEAKER2_INDEX = AAS.get_device_index_from_name('AB13X USB Audio')

AUDIO_DELAY = CL.get_config_value('advanced_audio_properties', ['audio_delay']) / 1000 # Convert milliseconds to seconds
SAMPLE_RATE = CL.get_config_value('advanced_audio_properties', ['sample_rate'])
BUFFER_SIZE = CL.get_config_value('advanced_audio_properties', ['chunk_size'])

WEBCAM_INDEX_1 = CL.get_config_value('webcams', ['webcam_1', 'index'])
WEBCAM_INDEX_2 = CL.get_config_value('webcams', ['webcam_2', 'index'])

#KT USB Audio
#AB13X USB Audio

MONITOR_INDEX_1 = 0
MONITOR_INDEX_2 = 1

VIDEO_DELAY = CL.get_config_value('advanced_video_properties', ['video_delay']) / 1000 # Convert milliseconds to seconds


# Buffers for delayed audio
audio_buffer_1 = []
audio_buffer_2 = []

phidget1 = DigitalInput()
phidget1_serial = 678328  # Replace with your Phidget 1 serial number
phidget1.setDeviceSerialNumber(phidget1_serial)
phidget1.setChannel(0)

phidget2 = DigitalInput()
phidget2_serial = 678505  # Replace with your Phidget 2 serial number
phidget2.setDeviceSerialNumber(phidget2_serial)
phidget2.setChannel(0)

# Global lock to ensure only one trigger function runs at a time
trigger_lock = threading.Lock()

station1_enabled = False
station2_enabled = False

station_lock = threading.Lock()

def station1_trigger():
    global station1_enabled
    with station_lock:
      try:
          print("Phidget 1: Button pressed - Recording & Playing")
          with sd.InputStream(device=MIC_INDEX_1, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE) as mic_stream, \
              sd.OutputStream(device=SPEAKER2_INDEX, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE) as speaker_stream:
              while station1_enabled:  # While the button is held
                  audio_chunk, _ = mic_stream.read(BUFFER_SIZE)  # Read from mic
                  audio_buffer_1.append(audio_chunk)  # Store in buffer

                  # Maintain delay buffer size
                  if len(audio_buffer_1) * (BUFFER_SIZE / SAMPLE_RATE) > AUDIO_DELAY:
                      delayed_audio = audio_buffer_1.pop(0)
                      speaker_stream.write(delayed_audio)  # Play delayed audio
      except sd.PortAudioError as e:
          print(f"Audio error (Phidget 1): {e}")

def station2_trigger():
    global station2_enabled
    with station_lock:
      try:
          print("Phidget 2: Button pressed - Recording & Playing")
          with sd.InputStream(device=MIC_INDEX_2, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE) as mic_stream, \
              sd.OutputStream(device=SPEAKER1_INDEX, channels=1, samplerate=SAMPLE_RATE, blocksize=BUFFER_SIZE) as speaker_stream:
              while station2_enabled:  # While the button is held
                  audio_chunk, _ = mic_stream.read(BUFFER_SIZE)  # Read from mic
                  audio_buffer_2.append(audio_chunk)  # Store in buffer

                  # Maintain delay buffer size
                  if len(audio_buffer_2) * (BUFFER_SIZE / SAMPLE_RATE) > AUDIO_DELAY:
                      delayed_audio = audio_buffer_2.pop(0)
                      speaker_stream.write(delayed_audio)  # Play delayed audio
      except sd.PortAudioError as e:
          print(f"Audio error (Phidget 2): {e}")

def phidget1_trigger(self, state):
    global station1_enabled
    if state:  # Button pressed
        if not station1_enabled:  # Check if not already enabled
            station1_enabled = True
            station1_thread = threading.Thread(target=station1_trigger)
            station1_thread.start()
    else:  # Button released
        station1_enabled = False
        time.sleep(0.1)  # Allow time for thread to properly terminate

def phidget2_trigger(self, state):
    global station2_enabled
    if state:  # Button pressed
        if not station2_enabled:  # Check if not already enabled
            station2_enabled = True
            station2_thread = threading.Thread(target=station2_trigger)
            station2_thread.start()
    else:  # Button released
        station2_enabled = False
        time.sleep(0.1)  # Allow time for thread to properly terminate

# Set up handlers
phidget1.setOnStateChangeHandler(phidget1_trigger)
phidget2.setOnStateChangeHandler(phidget2_trigger)

video_controller = videoController(WEBCAM_INDEX_1, WEBCAM_INDEX_2, MONITOR_INDEX_1, MONITOR_INDEX_2, video_delay=VIDEO_DELAY)
video_controller_thread = threading.Thread(target=video_controller.run)
video_controller_thread.start()
print("Video Controller Started")

# Open Phidgets
try:
    phidget1.openWaitForAttachment(5000)
    phidget2.openWaitForAttachment(5000)
    print("Phidgets attached. Waiting for button press...")

    while True:
      # Check for exit condition
      with video_controller.LOCK:
        if video_controller.EXIT:
          print("BREAKING")
          break
      time.sleep(0.1)  # Keep script running

except PhidgetException as e:
    print(f"Phidget error: {e}")

finally:
    phidget1.close()
    phidget2.close()
    print("Phidgets closed.")
