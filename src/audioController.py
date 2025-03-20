import pyaudio
from collections import deque
import sounddevice  # Must import to suppress ALSA config errors for some weird reason
import threading
from time import sleep

class microphone:
  def __init__(self, device_index, channels=1, rate=48000, chunk=2048, format=pyaudio.paInt16):
    self.device_index = device_index
    self.channels = channels
    self.rate = rate
    self.chunk = chunk
    self.format = format
    self.audio = pyaudio.PyAudio()
    self.stream = None

  def init(self):
    try:
      self.stream = self.audio.open(
        format=self.format,
        channels=self.channels,
        rate=self.rate,
        input=True,
        input_device_index=self.device_index,
        frames_per_buffer=self.chunk
      )
      return True
    except Exception as e:
      print(f"Error initializing microphone {self.device_index}: {e}")
      return False

  def getStream(self):
    return self.stream.read(self.chunk, exception_on_overflow=False)

  def close(self):
    if self.stream is not None:
      self.stream.stop_stream()
      self.stream.close()
    self.audio.terminate()

class speaker:
  def __init__(self, device_index, channels=1, rate=48000, chunk=2048, format=pyaudio.paInt16):
    self.device_index = device_index
    self.channels = channels
    self.rate = rate
    self.chunk = chunk
    self.format = format
    self.audio = pyaudio.PyAudio()
    self.stream = None

  def init(self):
    try:
      self.stream = self.audio.open(
          format=self.format,
          channels=self.channels,
          rate=self.rate,
          output=True,
          output_device_index=self.device_index,
          frames_per_buffer=self.chunk
        )
      return True
    except Exception as e:
      print(f"Error initializing speaker {self.device_index}: {e}")
      return False

  def play(self, data):
    self.stream.write(data)
    
  def close(self):
    if self.stream is not None:
      self.stream.stop_stream()
      self.stream.close()
    self.audio.terminate()

class audioController:
  def __init__(self, input_1, output_1, input_2, output_2, delay_duration=0, channels=1, rate=48000, chunk=2048, format=pyaudio.paInt16):
    self.input_1 = input_1
    self.output_1 = output_1
    self.input_2 = input_2
    self.output_2 = output_2
    self.delay_duration = delay_duration
    self.format = format
    self.channels = channels
    self.rate = rate
    self.chunk = chunk
    self.EXIT = False
    self.LOCK = threading.Lock()
    self.mute_spk_1 = True
    self.mute_spk_2 = True
    self.MUTE_LOCK = threading.Lock()

    # Buffers for delayed audio
    if self.delay_duration > 0:
      self.buffer_1 = deque(maxlen=int(self.rate / self.chunk * self.delay_duration))
      self.buffer_2 = deque(maxlen=int(self.rate / self.chunk * self.delay_duration))
    else:
      self.buffer_1 = None
      self.buffer_2 = None

    self.mic1 = None
    self.mic2 = None
    self.spk1 = None
    self.spk2 = None

  def init(self):
    self.mic1 = microphone(self.input_1, self.channels, self.rate, self.chunk, self.format)
    if not self.mic1.init():
      return False
    self.mic2 = microphone(self.input_2, self.channels, self.rate, self.chunk, self.format)
    if not self.mic2.init():
      return False
    self.spk1 = speaker(self.output_1, self.channels, self.rate, self.chunk, self.format)
    if not self.spk1.init():
      return False
    self.spk2 = speaker(self.output_2, self.channels, self.rate, self.chunk, self.format)
    if not self.spk2.init():
      return False
    return True

  def __close(self):
    if self.mic1:
      self.mic1.close()
    if self.mic2:
      self.mic2.close()
    if self.spk1:
      self.spk1.close()
    if self.spk2:
      self.spk2.close()
    print ("Audio controller closed.")

  def exit(self):
    with self.LOCK:
      self.EXIT = True
      
  def __updateStreams(self):
    # Read data from input streams
    data1 = self.mic1.getStream()
    data2 = self.mic2.getStream()

    if self.delay_duration > 0:
      # Add data to buffers
      self.buffer_1.append(data1)
      self.buffer_2.append(data2)

      # Get delayed data from buffers
      if len(self.buffer_1) == self.buffer_1.maxlen:
        delayed_data1 = self.buffer_1.popleft()
      else:
        delayed_data1 = b'\x00' * self.chunk * 2

      if len(self.buffer_2) == self.buffer_2.maxlen:
        delayed_data2 = self.buffer_2.popleft()
      else:
        delayed_data2 = b'\x00' * self.chunk * 2
    else:
      delayed_data1 = data1
      delayed_data2 = data2

    # Write delayed data to output streams
    with self.MUTE_LOCK:
      if not self.mute_spk_1:
        self.spk1.play(delayed_data1)
      if not self.mute_spk_2:
        self.spk2.play(delayed_data2)

  def set_spk1_Mute(self, mute):
    with self.MUTE_LOCK:
      self.mute_spk_1 = mute

  def set_spk2_Mute(self, mute):
    with self.MUTE_LOCK:
      self.mute_spk_2 = mute

  def run(self):
    try:
      if not self.init():
        print("Failed to initialize audio controller.")
        return

      with self.LOCK:
        self.EXIT = False

      while True:
        with self.LOCK:
          if self.EXIT:
            break
        self.__updateStreams()
    except IOError as e:
      print(f"Error: {e}")

    except KeyboardInterrupt:
      pass

    finally:
      self.__close()

# Example usage
"""
if __name__ == "__main__":
    audio_test = audioController(input_1=9, output_1=1, input_2=10, output_2=7, delay_duration=0)
    audioThread = threading.Thread(target=audio_test.run)
    audioThread.start()

    sleep(5)
    with audio_test.LOCK:
        audio_test.EXIT = True
    audioThread.join()
# """