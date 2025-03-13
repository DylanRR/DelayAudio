import static
import config

#Audio
import pyaudio
from collections import deque
import sounddevice     #Must import to supress ALSA config errors for some weird reason
import wave

#Video
import cv2
import time
from screeninfo import get_monitors

#Phidgets
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *

audio = None
input_stream_1 = None
input_stream_2 = None
output_stream_1 = None
output_stream_2 = None
buffer_1 = None
buffer_2 = None
FORMAT = None

def setup_audio():
  global audio, input_stream_1, input_stream_2, output_stream_1, output_stream_2, buffer_1, buffer_2, FORMAT
  audio = pyaudio.PyAudio()
  input_stream_1 = audio.open(
    format=FORMAT,
    channels=static.CHANNELS,
    rate=static.SAMPLE_RATE,
    input=True,
    input_device_index=static.MIC_1_INDEX,
    frames_per_buffer=static.CHUNK
)





webcam_1 = None
webcam_2 = None

def setup_webcams():
  global webcam_1, webcam_2

  # Open both webcams
  webcam_1 = cv2.VideoCapture(static.WEBCAM_1_INDEX)  # Webcam 1
  webcam_2 = cv2.VideoCapture(static.WEBCAM_2_INDEX)  # Webcam 2

  if not webcam_1.isOpened():
    print("Error: Could not open webcam 1.")
    return False
  if not webcam_2.isOpened():
    print("Error: Could not open webcam 2.")
    return False

  return True


monitor_1 = None
monitor_2 = None
monitor_1_width = None
monitor_1_height = None
monitor_2_width = None
monitor_2_height = None

def setup_monitors():
  global monitor_1, monitor_2, monitor_1_width, monitor_1_height, monitor_2_width, monitor_2_height

  monitors = get_monitors()

  if len(monitors) < 2:
    print("Error: Less than two monitors detected.")
    return

  # Assign monitors
  monitor_1 = monitors[0]  # Primary monitor
  monitor_2 = monitors[1]  # Secondary monitor

  # Monitor A properties
  monitor_1_width = monitor_1.width
  monitor_1_height = monitor_1.height
  monitor_1_x_position = monitor_1.x
  monitor_1_y_position = monitor_1.y

  # Monitor B properties
  monitor_2_width = monitor_2.width
  monitor_2_height = monitor_2.height
  monitor_2_x_position = monitor_2.x
  monitor_2_y_position = monitor_2.y

  # Create named windows
  cv2.namedWindow('Webcam 1', cv2.WINDOW_NORMAL)
  cv2.namedWindow('Webcam 2', cv2.WINDOW_NORMAL)

  # Move windows to respective monitors
  cv2.moveWindow('Webcam 1', monitor_1_x_position, monitor_1_y_position)
  cv2.moveWindow('Webcam 2', monitor_2_x_position, monitor_2_y_position)

  # Set windows to fullscreen
  time.sleep(1)  # Small delay to ensure window properties are applied
  cv2.setWindowProperty('Webcam 1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  cv2.setWindowProperty('Webcam 2', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def main():
    setup_webcams()
    setup_monitors()

    while True:
        # Capture frames from both webcams
        ret1, frame1 = webcam_1.read()
        ret2, frame2 = webcam_2.read()

        if not ret1:
            print("Error: Could not read frame from webcam 1.")
            break
        if not ret2:
            print("Error: Could not read frame from webcam 2.")
            break

        # Resize frames to fit respective screens
        frame1 = cv2.resize(frame1, (monitor_1_width, monitor_1_height))
        frame2 = cv2.resize(frame2, (monitor_2_width, monitor_2_height))

        # Display frames
        cv2.imshow('Webcam 1', frame1)
        cv2.imshow('Webcam 2', frame2)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release the captures and close the windows
    webcam_1.release()
    webcam_2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
