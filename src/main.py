from audioController import audioController
from videoController import videoController
from phidgetController import phidgetController
import threading
import time
import sys
import os
import select

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import configuration_loader_v2 as configuration_loader
from config import advancedAudioScan as AAS
from config import advancedWebcamScan as AWS

try:
  config_path = configuration_loader.get_config_path()
  CL = configuration_loader.ConfigurationLoader(config_path)
  PHIDGET_1_SERIAL_NUMBER = CL.get_config_value('phidgets', ['phidget_1', 'serial_number'])
  PHIDGET_2_SERIAL_NUMBER = CL.get_config_value('phidgets', ['phidget_2', 'serial_number'])
  PHIDGET_1_CHANNELS = CL.get_config_value('phidgets', ['phidget_1', 'active_channels'])
  PHIDGET_2_CHANNELS = CL.get_config_value('phidgets', ['phidget_2', 'active_channels'])
  
  
  MIC_INDEX_1 = CL.get_config_value('microphones', ['microphone_1', 'index'])
  MIC_INDEX_2 = CL.get_config_value('microphones', ['microphone_2', 'index'])

  #MIC_INDEX_1 = AAS.get_card_index_from_serial('MVX2U#2-b71cdcfb0cbedc549200ce724ab01ba6')
  #MIC_INDEX_2 = AAS.get_card_index_from_serial('MVX2U#2-b71cdcfb0cbedc549200ce724ab01ba6')
  
  SPEAKER_INDEX_1 = CL.get_config_value('speakers', ['speaker_1', 'index'])
  SPEAKER_INDEX_2 = CL.get_config_value('speakers', ['speaker_2', 'index'])
  
  """
  WEBCAM_INDEX_1 = CL.get_config_value('webcams', ['webcam_1', 'index'])
  WEBCAM_INDEX_2 = CL.get_config_value('webcams', ['webcam_2', 'index'])
  """
  WEBCAM_INDEX_1 = AWS.get_cv2_index_from_serial('89DD42EF')
  WEBCAM_INDEX_2 = AWS.get_cv2_index_from_serial('A55D42EF')
  
  MONITOR_INDEX_1 = CL.get_config_value('monitors', ['monitor_1', 'index'])
  MONITOR_INDEX_2 = CL.get_config_value('monitors', ['monitor_2', 'index'])
  AUDIO_DELAY = CL.get_config_value('advanced_audio_properties', ['audio_delay'])
  AUDIO_DELAY = AUDIO_DELAY / 1000  # Convert milliseconds to seconds
  SAMPLE_RATE = CL.get_config_value('advanced_audio_properties', ['sample_rate'])
  AUDIO_CHANNELS = CL.get_config_value('advanced_audio_properties', ['audio_channels'])
  CHUNK_SIZE = CL.get_config_value('advanced_audio_properties', ['chunk_size'])
  VIDEO_DELAY = CL.get_config_value('advanced_video_properties', ['video_delay'])
  VIDEO_DELAY = VIDEO_DELAY / 1000  # Convert milliseconds to seconds
  
except Exception as e:
  print(f"Error loading configuration Data: {e}")
  exit(1)


if __name__ == "__main__":
  try: 
    video_controller = videoController(WEBCAM_INDEX_1, WEBCAM_INDEX_2, MONITOR_INDEX_1, MONITOR_INDEX_2, video_delay=VIDEO_DELAY)
    video_controller_thread = threading.Thread(target=video_controller.run)
    video_controller_thread.start()
    print("Video Controller Started")

    audio_controller = audioController(input_1=MIC_INDEX_1, output_1=SPEAKER_INDEX_1, input_2=MIC_INDEX_2, output_2=SPEAKER_INDEX_2, delay_duration=AUDIO_DELAY, channels=AUDIO_CHANNELS, rate=SAMPLE_RATE, chunk=CHUNK_SIZE)
    audioThread = threading.Thread(target=audio_controller.run)
    audioThread.start()
    print ("Audio Controller Started")

    phidget1 = phidgetController(serial_number=PHIDGET_1_SERIAL_NUMBER, channels=PHIDGET_1_CHANNELS)
    phidget2 = phidgetController(serial_number=PHIDGET_2_SERIAL_NUMBER, channels=PHIDGET_2_CHANNELS)

    if not phidget1.init():
      print("Failed to initialize Phidget 1.")
      exit(1)
    else:
      print("Phidget Controller 1 Stated")

    if not phidget2.init():
      print("Failed to initialize Phidget 2.")
      exit(1)
    else:
      print("Phidget Controller 2 Stated")
      
      
  except Exception as e:
    print(f"Exception: {e}")

  tempSpk1Mute = True
  tempSpk2Mute = True

  print("Starting main loop...")
  
  def spk1Mute():
    global tempSpk1Mute
    print("spk1Mute")
    audio_controller.set_spk1_Mute(True)
    tempSpk1Mute = True
  
  def spk2Mute():
    global tempSpk2Mute
    print("spk2Mute")
    audio_controller.set_spk2_Mute(True)
    tempSpk2Mute = True
    
    
  spk1Mute()
  spk2Mute()
    
  try:
    while True:
      
      if phidget1.is_button_pressed(0):
        audio_controller.set_spk1_Mute(False)
        while phidget1.is_button_pressed(0):
          with video_controller.LOCK:
            if video_controller.EXIT:
              print("BREAKING")
              break
        timer = threading.Timer(AUDIO_DELAY, spk1Mute)
        timer.start()
        
      if phidget2.is_button_pressed(0):
        audio_controller.set_spk2_Mute(False)
        while phidget2.is_button_pressed(0):
          with video_controller.LOCK:
            if video_controller.EXIT:
              print("BREAKING")
              break
        timer2 = threading.Timer(AUDIO_DELAY, spk2Mute)
        timer2.start()
      
          
      # Check for exit condition
      with video_controller.LOCK:
        if video_controller.EXIT:
          print("BREAKING")
          break
      
      time.sleep(0.01)
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
    print ("Successfully closed all threads.")

