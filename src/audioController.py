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

  def init(self):
    self.stream = self.audio.open(
      format=self.format,
      channels=self.channels,
      rate=self.rate,
      input=True,
      input_device_index=self.device_index,
      frames_per_buffer=self.chunk
    )

  def getStream(self):
    return self.stream.read(self.chunk, exception_on_overflow=False)

  def close(self):
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

  def init(self):
    self.stream = self.audio.open(
      format=self.format,
      channels=self.channels,
      rate=self.rate,
      output=True,
      output_device_index=self.device_index,
      frames_per_buffer=self.chunk
    )

  def play(self, data):
    self.stream.write(data)

  def close(self):
    self.stream.stop_stream()
    self.stream.close()
    self.audio.terminate()

class audioController:
  def __init__(self, input_1, output_1, input_2, output_2, delay_duration=2.5, format=pyaudio.paInt16, channels=1, rate=48000, chunk=2048):
    self.input_1 = input_1
    self.output_1 = output_1
    self.input_2 = input_2
    self.output_2 = output_2
    self.delay_duration = delay_duration
    self.format = format
    self.channels = channels
    self.rate = rate
    self.chunk = chunk
    self.exit = False
    self.LOCK = threading.Lock()

    # Buffers for delayed audio
    self.buffer_1 = deque(maxlen=int(self.rate / self.chunk * self.delay_duration))
    self.buffer_2 = deque(maxlen=int(self.rate / self.chunk * self.delay_duration))

    self.mic1 = None
    self.mic2 = None
    self.spk1 = None
    self.spk2 = None

  def init(self):
    self.mic1 = microphone(self.input_1, self.channels, self.rate, self.chunk, self.format)
    self.mic1.init()
    self.mic2 = microphone(self.input_2, self.channels, self.rate, self.chunk, self.format)
    self.mic2.init()
    self.spk1 = speaker(self.output_1, self.channels, self.rate, self.chunk, self.format)
    self.spk1.init()
    self.spk2 = speaker(self.output_2, self.channels, self.rate, self.chunk, self.format)
    self.spk2.init()

  def cleanup(self):
    self.mic1.close()
    self.mic2.close()
    self.spk1.close()
    self.spk2.close()

  def run(self):
    try:
      with self.LOCK:
          self.exit = False

      while True:
        try:
            with self.LOCK:
              if self.exit:
                break

            # Read data from input streams
            data1 = self.mic1.getStream()
            data2 = self.mic2.getStream()

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

            # Write delayed data to output streams
            self.spk1.play(delayed_data2)
            self.spk2.play(delayed_data1)

        except IOError as e:
            print(f"Error: {e}")

    except KeyboardInterrupt:
        pass

    finally:
        self.cleanup()

if __name__ == "__main__":
  audio_test = audioController(input_1=0, output_1=9, input_2=1, output_2=10)
  audio_test.init()
  audioThread = threading.Thread(target=audio_test.run)
  audioThread.start()

  sleep(10)
  with audio_test.LOCK:
      audio_test.exit = True
  audioThread.join()