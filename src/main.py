from audioController import audioController
from videoController import videoController
from phidgetController import phidgetController
import configuration_loader
import threading
import time
import os

try:
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  CL = configuration_loader.ConfigurationLoader(config_path)
  WEBCAM_INDEX_1 = CL.get_webcam_index('webcam_1')
  WEBCAM_INDEX_2 = CL.get_webcam_index('webcam_2')
  MONITOR_INDEX_1 = CL.get_monitor_index('monitor_1')
  MONITOR_INDEX_2 = CL.get_monitor_index('monitor_2')
  MIC_INDEX_1 = CL.get_microphone_index('microphone_1')
  MIC_INDEX_2 = CL.get_microphone_index('microphone_2')
  SPEAKER_INDEX_1 = CL.get_speaker_index('speaker_1')
  SPEAKER_INDEX_2 = CL.get_speaker_index('speaker_2')
  PHIDGET_1_SERIAL_NUMBER = CL.get_phidget_serial('phidget_1')
  PHIDGET_2_SERIAL_NUMBER = CL.get_phidget_serial('phidget_2')
  PHIDGET_1_CHANNELS = CL.get_phidget_channels('phidget_1')
  PHIDGET_2_CHANNELS = CL.get_phidget_channels('phidget_2')
  VIDEO_DELAY = CL.get_advanced_video_options('video_delay')
  AUDIO_DELAY = CL.get_advanced_audio_options('audio_delay')
  SAMPLE_RATE = CL.get_advanced_audio_options('sample_rate')
  AUDIO_CHANNELS = CL.get_advanced_audio_options('audio_channels')
  CHUNK_SIZE = CL.get_advanced_audio_options('chunk_size')
except Exception as e:
  print(f"Error loading configuration Data: {e}")
  exit(1)

if __name__ == "__main__":
  video_controller = videoController(WEBCAM_INDEX_1, WEBCAM_INDEX_2, MONITOR_INDEX_1, MONITOR_INDEX_2, video_delay=VIDEO_DELAY)
  video_controller_thread = threading.Thread(target=video_controller.run)
  video_controller_thread.start()
  print("Video Controller Started")

  audio_controller = audioController(input_1=MIC_INDEX_1, output_1=SPEAKER_INDEX_1, input_2=MIC_INDEX_1, output_2=SPEAKER_INDEX_2, delay_duration=AUDIO_DELAY, channels=AUDIO_CHANNELS, rate=SAMPLE_RATE, chunk=CHUNK_SIZE)
  audioThread = threading.Thread(target=audio_controller.run)
  audioThread.start()
  print ("Audio Controller Started")

  phidget1 = phidgetController(serial_number=PHIDGET_1_SERIAL_NUMBER, channels=PHIDGET_1_CHANNELS)
  phidget2 = phidgetController(serial_number=PHIDGET_2_SERIAL_NUMBER, channels=PHIDGET_2_CHANNELS)

  if not phidget1.init():
    print("Failed to initialize Phidget 1.")
    exit(1)
  if not phidget2.init():
    print("Failed to initialize Phidget 2.")
    exit(1)


  tempSpk1Mute = True
  tempSpk2Mute = True

  try:
    while True:
      if phidget1.is_button_pressed(0):
        if tempSpk1Mute:
          audio_controller.set_spk1_Mute(False)
          tempSpk1Mute = False
      else:
        if not tempSpk1Mute:
          audio_controller.set_spk1_Mute(True)
          tempSpk1Mute = True

      if phidget2.is_button_pressed(0):
        if tempSpk2Mute:
          audio_controller.set_spk2_Mute(False)
          tempSpk2Mute = False
      else:
        if not tempSpk2Mute:
          audio_controller.set_spk2_Mute(True)
          tempSpk2Mute = True
      time.sleep(0.1)
  except Exception as e:
    print(f"Exception: {e}")
  except KeyboardInterrupt:
    print("KeyboardInterrupt detected. Exiting...")
  finally:
    video_controller.exit()
    video_controller_thread.join()
    audio_controller.exit()
    audioThread.join()
    phidget1.close()
    phidget2.close()

