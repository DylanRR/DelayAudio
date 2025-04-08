import cv2
import time
from screeninfo import get_monitors
import threading
from collections import deque
import os

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
  def __init__(self, webcam_1, webcam_2, monitor_1, monitor_2, video_delay=0):
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

    self.video_delay = video_delay
    if self.video_delay > 0:
      self.buffer_1 = deque(maxlen=int(self.video_delay * 30))  # Assuming 30 FPS
      self.buffer_2 = deque(maxlen=int(self.video_delay * 30))  # Assuming 30 FPS
    else:
      self.buffer_1 = None
      self.buffer_2 = None


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
    print ("Video controller closed.")

  def exit(self):
    with self.LOCK:
      self.EXIT = True

  def __show_frames(self):
    frame1 = self.webcam_2.get_frame()
    frame2 = self.webcam_1.get_frame()

    if self.video_delay > 0:
      self.__process_delayed_frames(frame1, frame2)
    else:
      overlay_images_frame1 = [("lunar_base.png", "upper_left"), ("desc.png", "lower_right")]
      overlay_images_frame2 = [("mission_control.png", "upper_left"), ("desc.png", "lower_right")]
      self.__display_frame(self.monitor_1, frame1, overlay_images_frame1)
      self.__display_frame(self.monitor_2, frame2, overlay_images_frame2)

  def __process_delayed_frames(self, frame1, frame2):
    self.buffer_1.append(frame1)
    self.buffer_2.append(frame2)

    if len(self.buffer_1) == self.buffer_1.maxlen:
      delayed_frame1 = self.buffer_1.popleft()
      overlay_images_frame1 = [("lunar_base.png", "upper_left"), ("desc.png", "lower_right")]
      self.__display_frame(self.monitor_1, delayed_frame1, overlay_images_frame1)

    if len(self.buffer_2) == self.buffer_2.maxlen:
      delayed_frame2 = self.buffer_2.popleft()
      overlay_images_frame2 = [("mission_control.png", "upper_left"), ("desc.png", "lower_right")]
      self.__display_frame(self.monitor_2, delayed_frame2, overlay_images_frame2)

  def __display_frame(self, monitor, frame, overlay_images):
    if frame is not None:
      frame = self.__add_image_overlays(frame, overlay_images)
      monitor.show_frame(frame)
    else:
      print(f"No frame captured.")

  def __add_image_overlays(self, frame, overlay_images):
    for overlay_image_path, position in overlay_images:
      # Get the absolute path of the PNG file
      overlay_image_path = os.path.join(os.path.dirname(__file__), overlay_image_path)

      # Load the PNG image
      overlay_image = cv2.imread(overlay_image_path, cv2.IMREAD_UNCHANGED)
      if overlay_image is None:
        print(f"Error: {overlay_image_path} not found.")
        continue

      # Check if the overlay image has an alpha channel
      has_alpha = overlay_image.shape[2] == 4

      # Resize the overlay image if necessary
      overlay_height, overlay_width = overlay_image.shape[:2]
      if overlay_height > frame.shape[0] or overlay_width > frame.shape[1]:
        scale = min(frame.shape[0] / overlay_height, frame.shape[1] / overlay_width)
        overlay_image = cv2.resize(overlay_image, (int(overlay_width * scale), int(overlay_height * scale)))

      # Determine the region of interest (ROI) in the frame
      if position == "upper_left":
        roi = frame[0:overlay_image.shape[0], 0:overlay_image.shape[1]]
      elif position == "lower_right":
        roi = frame[-overlay_image.shape[0]:, -overlay_image.shape[1]:]

      if has_alpha:
        # Extract the alpha channel and the color channels
        alpha_channel = overlay_image[:, :, 3] / 255.0
        color_channels = overlay_image[:, :, :3]

        # Blend the overlay image with the ROI using the alpha channel
        for c in range(3):  # Iterate over the color channels
          roi[:, :, c] = (1 - alpha_channel) * roi[:, :, c] + alpha_channel * color_channels[:, :, c]
      else:
        # If no alpha channel, directly overlay the image
        roi[:, :, :] = overlay_image[:, :, :3]

      # Replace the ROI in the frame with the blended or overlaid result
      if position == "upper_left":
        frame[0:overlay_image.shape[0], 0:overlay_image.shape[1]] = roi
      elif position == "lower_right":
        frame[-overlay_image.shape[0]:, -overlay_image.shape[1]:] = roi

    return frame

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
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Escape key
          self.exit()
          break

    except IOError as e:
      print(f"Error: {e}")
    finally:
      self.__close()



# Example usage
"""
if __name__ == "__main__":
  video_controller = videoController(0, 2, 0, 1, video_delay=0)

  video_controller_thread = threading.Thread(target=video_controller.run)
  video_controller_thread.start()
  print("Main Thread")
  time.sleep(10)
  with video_controller.LOCK:
    video_controller.EXIT = True
  video_controller_thread.join()
# """

