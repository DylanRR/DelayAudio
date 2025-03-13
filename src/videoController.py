import cv2
import time
from screeninfo import get_monitors
import threading

class webcam:
  def __init__(self, device_index):
    self.index = device_index
    self.video_capture = None

  def init(self):
    self.video_capture = cv2.VideoCapture(self.index)
    if not self.video_capture.isOpened():
      print(f"Error: Could not open webcam {self.index}.")
      return False
    return True

  def close(self):
    self.index = None
    if self.video_capture is not None:
      self.video_capture.release()

  def get_frame(self):
    ret, frame = self.video_capture.read()
    if not ret:
      print(f"Error: Could not read frame from webcam {self.index}.")
      return None
    return frame

class monitor:
  def __init__(self, device_index):
    self.index = device_index
    self.monitor = None
    self.width = None
    self.height = None
    self.x_position = None
    self.y_position = None

  def init(self):
    monitors = get_monitors()
    if len(monitors) <= self.index:
      print(f"Error: Monitor {self.index} not detected.")
      return False

    self.monitor = monitors[self.index]
    self.width = self.monitor.width
    self.height = self.monitor.height
    self.x_position = self.monitor.x
    self.y_position = self.monitor.y

    cv2.namedWindow(f'Monitor {self.index}', cv2.WINDOW_NORMAL)
    cv2.moveWindow(f'Monitor {self.index}', self.x_position, self.y_position)
    time.sleep(1)  # Small delay to ensure window properties are applied
    cv2.setWindowProperty(f'Monitor {self.index}', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    return True

  def close(self):
    self.monitor = None
    self.width = None
    self.height = None
    self.x_position = None
    self.y_position = None
    cv2.destroyWindow(f'Monitor {self.index}')

  def show_frame(self, frame):
    frame = cv2.resize(frame, (self.width, self.height))
    cv2.imshow(f'Monitor {self.index}', frame)
    cv2.waitKey(1)  # Allow OpenCV to process window events

class videoController:
  def __init__(self, webcam_1, webcam_2, monitor_1, monitor_2):
    self.webcam_1_index = webcam_1
    self.webcam_2_index = webcam_2
    self.monitor_1_index = monitor_1
    self.monitor_2_index = monitor_2

    self.webcam_1 = None
    self.webcam_2 = None
    self.monitor_1 = None
    self.monitor_2 = None

    self.EXIT = False
    self.LOCK = threading.Lock()

  def init(self):
    self.webcam_1 = webcam(self.webcam_1_index)
    if not self.webcam_1.init():
      print("Failed to initialize webcam 1.")
      return False

    self.webcam_2 = webcam(self.webcam_2_index)
    if not self.webcam_2.init():
      print("Failed to initialize webcam 2.")
      return False

    self.monitor_1 = monitor(self.monitor_1_index)
    if not self.monitor_1.init():
      print("Failed to initialize monitor 1.")
      return False

    self.monitor_2 = monitor(self.monitor_2_index)
    if not self.monitor_2.init():
      print("Failed to initialize monitor 2.")
      return False

    return True

  def __close(self):
    self.webcam_1.close()
    self.webcam_2.close()
    self.monitor_1.close()
    self.monitor_2.close()

  def __show_frames(self):
    frame1 = self.webcam_1.get_frame()
    frame2 = self.webcam_2.get_frame()

    if frame1 is not None:
      self.monitor_1.show_frame(frame1)
    else:
      print("No frame captured from webcam 1.")

    if frame2 is not None:
      self.monitor_2.show_frame(frame2)
    else:
      print("No frame captured from webcam 2.")

  def run(self):
    try:
      if not self.init():
        print("Failed to initialize video controller.")
        return
      
      with self.LOCK:
        self.EXIT = False

      while True:
        with self.LOCK:
          if self.EXIT:
            break
        self.__show_frames()

    except IOError as e:
      print(f"Error: {e}")
    finally:
      self.__close()


if __name__ == "__main__":
  video_controller = videoController(0, 2, 0, 1)

  video_controller_thread = threading.Thread(target=video_controller.run)
  video_controller_thread.start()
  print("Main Thread")
  time.sleep(10)
  with video_controller.LOCK:
    video_controller.EXIT = True
  video_controller_thread.join()


