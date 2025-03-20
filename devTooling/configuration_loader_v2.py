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
  
  
  def set_config_value(self, section, key, value):
    """
    Updates a specific key in the configuration file and saves the changes.

    Args:
        section (str): The top-level section in the configuration (e.g., 'phidgets', 'microphones').
        key (str or list): The key or path within the section to update. If nested, pass a list of keys (e.g., ['phidget_1', 'channels']).
        value: The new value to set for the specified key.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    # Ensure the configuration is loaded
    if not self.config:
        print("Configuration not loaded. Cannot set value.")
        return False

    # Check if the section exists in the configuration
    if section not in self.config:
        print(f"Section '{section}' does not exist in the configuration.")
        return False

    # Navigate to the correct key if it's nested
    current_level = self.config[section]
    if isinstance(key, list):
        for subkey in key[:-1]:  # Traverse all but the last key
            if subkey not in current_level:
                print(f"Key '{subkey}' does not exist in section '{section}'.")
                return False
            current_level = current_level[subkey]
        final_key = key[-1]
    else:
        final_key = key

    # Convert the value to an integer if the existing value is an integer
    if final_key in current_level and isinstance(current_level[final_key], int):
        try:
            value = int(value)  # Attempt to convert the value to an integer
        except (ValueError, TypeError):
            print(f"Failed to convert value '{value}' to an integer for key '{final_key}'.")
            return False

    # Update the value
    if final_key in current_level:
        current_level[final_key] = value
    else:
        print(f"Key '{final_key}' does not exist in section '{section}'.")
        return False

    # Save the updated configuration back to the file
    try:
        with open(self.file_path, 'w') as file:
            json.dump(self.config, file, indent=4)
        print(f"Successfully updated '{final_key}' in section '{section}' to '{value}'.")
        return True
    except Exception as e:
        print(f"Error saving updated configuration: {e}")
        return False
  
  def get_config_value(self, section, key):
    """
    Retrieves a specific value from the configuration file.

    Args:
        section (str): The top-level section in the configuration (e.g., 'phidgets', 'microphones').
        key (str or list): The key or path within the section to retrieve. If nested, pass a list of keys (e.g., ['phidget_1', 'channels']).

    Returns:
        The value if found, or None if the section or key does not exist.
    """
    # Ensure the configuration is loaded
    if not self.config:
        print("Configuration not loaded. Cannot get value.")
        return None

    # Check if the section exists in the configuration
    if section not in self.config:
        print(f"Section '{section}' does not exist in the configuration.")
        return None

    # Navigate to the correct key if it's nested
    current_level = self.config[section]
    if isinstance(key, list):
        for subkey in key:  # Traverse through all keys in the list
            if subkey not in current_level:
                print(f"Key '{subkey}' does not exist in section '{section}'.")
                return None
            current_level = current_level[subkey]
        return current_level  # Return the final value
    else:
        # If the key is a string, return the value directly
        return current_level.get(key, None)
  

  
  def is_config_valid(self):
      # Define the required structure of the configuration file
      required_structure = {
          "phidgets": {
              "phidget_1": {"serial_number": None, "active_channels": []},
              "phidget_2": {"serial_number": None, "active_channels": []}
          },
          "microphones": {
              "microphone_1": {"index": None},
              "microphone_2": {"index": None}
          },
          "speakers": {
              "speaker_1": {"index": None},
              "speaker_2": {"index": None}
          },
          "webcams": {
              "webcam_1": {"index": None},
              "webcam_2": {"index": None}
          },
          "monitors": {
              "monitor_1": {"index": None},
              "monitor_2": {"index": None}
          },
          "advanced_audio_properties": {
              "audio_delay": None,
              "sample_rate": None,
              "audio_channels": None,
              "chunk_size": None
          },
          "advanced_video_properties": {
              "video_delay": None
          }
      }

      # Recursively check if the actual configuration matches the expected structure
      def check_keys(expected, actual):
          if not isinstance(expected, dict):  # Leaf node
              return True
          if not isinstance(actual, dict):  # If the actual value is not a dictionary, the structure is invalid
              return False
          
          for key, subkeys in expected.items(): # Iterate through all keys in the expected structure
              if key not in actual: # Check if the key exists in the actual configuration
                  return False
              if not check_keys(subkeys, actual[key]):  # Recursively check the subkeys
                  return False
          return True # If all keys and subkeys match, return True

      # Call the recursive function with the required structure and the loaded configuration
      return check_keys(required_structure, self.config)
    
  def rebuild_config_file(self):
    # Define the default configuration structure
    default_config = {
        "phidgets": {
            "phidget_1": {"serial_number": None, "active_channels": []},
            "phidget_2": {"serial_number": None, "active_channels": []}
        },
        "microphones": {
            "microphone_1": {"index": None},
            "microphone_2": {"index": None}
        },
        "speakers": {
            "speaker_1": {"index": None},
            "speaker_2": {"index": None}
        },
        "webcams": {
            "webcam_1": {"index": None},
            "webcam_2": {"index": None}
        },
        "monitors": {
            "monitor_1": {"index": None},
            "monitor_2": {"index": None}
        },
        "advanced_audio_properties": {
            "audio_delay": None,
            "sample_rate": None,
            "audio_channels": None,
            "chunk_size": None
        },
        "advanced_video_properties": {
            "video_delay": None
        }
    }

    # Write the default configuration to the file
    with open(self.file_path, 'w') as file:
      json.dump(default_config, file, indent=4)
      
      
def is_valid_int_list_string(input_string):
  """
  Validates if a string contains only numbers, spaces, or commas.

  Args:
      input_string (str): The string to validate.

  Returns:
      bool: True if the string is valid, False otherwise.
  """
  valid_characters = set("0123456789, ")
  return all(char in valid_characters for char in input_string)
      
def string_to_int_list(input_string):
    """
    Converts a string of numbers separated by commas or spaces into a list of integers.
    Handles multiple spaces by replacing them with a single space.

    Args:
        input_string (str): A string of numbers separated by commas or spaces.

    Returns:
        list: A list of integers converted from the input string.
    """
    try:
        # Replace multiple spaces with a single space
        input_string = ' '.join(input_string.split())
        # Replace spaces with commas to standardize the delimiter
        input_string = input_string.replace(' ', ',')
        # Split the string by commas and convert each part to an integer
        return [int(item) for item in input_string.split(',') if item]
    except ValueError as e:
        print(f"Error converting string to list of integers: {e}")
        return []

  

# Example usage
"""
if __name__ == "__main__":
  
  '''
  Example usage to load and validate the configuration file
  This example assumes the configuration file is named 'config.json' and is located in the same directory as this script.
  '''
  # Use an absolute path to the config.json file
  config_path = os.path.join(os.path.dirname(__file__), 'config.json')
  config_loader = ConfigurationLoader(config_path)

  if config_loader.is_config_valid():  # Call the method on the instance
    print("Configuration is valid.")
  else:
    print("Configuration is invalid.")
    
    
  '''
  Example usage to set values
  This example sets the active channels to a list of integers and the serial number to an integer.
  Note: The actual values should be replaced with the desired values.
  '''  
  test_set = 1234
  test_channels = [1, 2, 3]
  
  if config_loader.set_config_value('phidgets', ['phidget_1', 'active_channels'], test_channels):
    print("Value set successfully.")
  else:
    print("Failed to set value.")
  
  if config_loader.set_config_value('phidgets', ['phidget_1', 'serial_number'], test_set):
    print("Value set successfully.")
  else:
    print("Failed to set value.")
    
  
  '''
  Example usage to get values
  '''
  print (config_loader.get_config_value('phidgets', ['phidget_1', 'active_channels']))
  print (config_loader.get_config_value('phidgets', ['phidget_1', 'serial_number']))
  print (config_loader.get_config_value('advanced_audio_properties', ['audio_delay']))

  '''
  Example usage test and convert string to int list
  '''
  testString0 = "1@,2,3,4a"
  print (is_valid_int_list_string(testString0))  # Output: False
  
  testString1 = "1,2,3,4"
  print (is_valid_int_list_string(testString1))  # Output: True
  print (string_to_int_list(testString1))  # Output: [1, 2, 3, 4]
  
  testString2 = "1, 2, 3, 4"
  print (is_valid_int_list_string(testString2))  # Output: True
  print (string_to_int_list(testString2))  # Output: [1, 2, 3, 4]
  
  testString3 = "1,2,3,4,"
  print (is_valid_int_list_string(testString3))  # Output: True
  print (string_to_int_list(testString3))  # Output: [1, 2, 3, 4]

# """
