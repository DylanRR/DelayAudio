import json
import os

class ConfigurationLoader:
  def __init__(self, file_path):
      self.file_path = file_path
      self.config = self.load_config()

  def load_config(self):
    try:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Configuration file not found: {self.file_path}")
        with open(self.file_path, 'r') as file:
            try:
                config = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON from configuration file: {e}")
        return config
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return None

  def get_phidget_serial(self, phidget_name):
      if self.config:
          return self.config.get('phidgets', {}).get(phidget_name, {}).get('serial_number', None)
      return None
  
  def get_phidget_channels(self, phidget_name):
      if self.config:
          return self.config.get('phidgets', {}).get(phidget_name, {}).get('active_channels', [])
      return []
  
  def get_microphone_index(self, mic_name):
      if self.config:
          return self.config.get('microphones', {}).get(mic_name, {}).get('index', None)
      return None
  
  def get_speaker_index(self, spk_name):
      if self.config:
          return self.config.get('speakers', {}).get(spk_name, {}).get('index', None)
      return None
  
  def get_webcam_index(self, cam_name):
      if self.config:
          return self.config.get('webcams', {}).get(cam_name, {}).get('index', None)
      return None
  
  def get_monitor_index(self, mon_name):
      if self.config:
          return self.config.get('monitors', {}).get(mon_name, {}).get('index', None)
      return None
  
  def get_advanced_audio_options(self, advanced_properties):
      if self.config:
          if isinstance(advanced_properties, list):
              return {prop: self.config.get('advanced_audio_properties', {}).get(prop, None) for prop in advanced_properties}
          else:
              return self.config.get('advanced_audio_properties', {}).get(advanced_properties, None)
      if isinstance(advanced_properties, list):
          return {prop: None for prop in advanced_properties}
      return None
  
  def get_advanced_video_options(self, advanced_properties):
      if self.config:
          if isinstance(advanced_properties, list):
              return {prop: self.config.get('advanced_video_properties', {}).get(prop, None) for prop in advanced_properties}
          else:
              return self.config.get('advanced_video_properties', {}).get(advanced_properties, None)
      if isinstance(advanced_properties, list):
          return {prop: None for prop in advanced_properties}
      return None

# Example usage
if __name__ == "__main__":
    # Use an absolute path to the config.json file
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    config_loader = ConfigurationLoader(config_path)
    
    # Get advanced audio options
    advanced_audio_properties = ['sample_rate', 'audio_channels', 'chunk_size', 'audio_delay']
    audio_options = config_loader.get_advanced_audio_options(advanced_audio_properties)
    print("Advanced Audio Options:", audio_options)
    
    # Get a single advanced audio option
    sample_rate = config_loader.get_advanced_audio_options('sample_rate')
    print("Sample Rate:", sample_rate)
    
    # Get advanced video options
    advanced_video_properties = ['video_delay']
    video_options = config_loader.get_advanced_video_options(advanced_video_properties)
    print("Advanced Video Options:", video_options)
    
    # Get a single advanced video option
    video_delay = config_loader.get_advanced_video_options('video_delay')
    print("Video Delay:", video_delay)
    
    # Get Phidget serial numbers and channels
    phidget1_serial = config_loader.get_phidget_serial('phidget_1')
    phidget2_serial = config_loader.get_phidget_serial('phidget_2')
    print(f"Phidget1 Serial Number: {phidget1_serial}")
    print(f"Phidget2 Serial Number: {phidget2_serial}")
    
    phidget1_channels = config_loader.get_phidget_channels('phidget_1')
    phidget2_channels = config_loader.get_phidget_channels('phidget_2')
    print(f"Phidget1 Channels: {phidget1_channels}")
    print(f"Phidget2 Channels: {phidget2_channels}")
    
    # Get microphone indices
    mic1_index = config_loader.get_microphone_index('microphone_1')
    mic2_index = config_loader.get_microphone_index('microphone_2')
    print(f"Microphone1 Index: {mic1_index}")
    print(f"Microphone2 Index: {mic2_index}")
    
    # Get speaker indices
    spk1_index = config_loader.get_speaker_index('speaker_1')
    spk2_index = config_loader.get_speaker_index('speaker_2')
    print(f"Speaker1 Index: {spk1_index}")
    print(f"Speaker2 Index: {spk2_index}")
    
    # Get webcam indices
    cam1_index = config_loader.get_webcam_index('webcam_1')
    cam2_index = config_loader.get_webcam_index('webcam_2')
    print(f"Webcam1 Index: {cam1_index}")
    print(f"Webcam2 Index: {cam2_index}")