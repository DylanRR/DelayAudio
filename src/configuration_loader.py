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
"""
if __name__ == "__main__":
  # Use an absolute path to the config.json file
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  config_loader = ConfigurationLoader(config_path)

  print("Phidget 1 Serial Number:", config_loader.get_phidget_serial('phidget_1'))
  print("Phidget 1 Channels:", config_loader.get_phidget_channels('phidget_1'))
  print("Microphone 1 Index:", config_loader.get_microphone_index('mic_1'))
  print("Speaker 1 Index:", config_loader.get_speaker_index('speaker_1'))
  print("Webcam 1 Index:", config_loader.get_webcam_index('webcam_1'))
  print("Monitor 1 Index:", config_loader.get_monitor_index('monitor_1'))
  print("Audio Delay:", config_loader.get_advanced_audio_options('audio_delay'))

# """
    