import cv2
import time
from screeninfo import get_monitors
import threading
from collections import deque

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
      self.__process_live_frames(frame1, frame2)

  def __process_delayed_frames(self, frame1, frame2):
    self.buffer_1.append(frame1)
    self.buffer_2.append(frame2)

    if len(self.buffer_1) == self.buffer_1.maxlen:
      delayed_frame1 = self.buffer_1.popleft()
      self.__display_frame(self.monitor_1, delayed_frame1, "LUNAR BASE")

    if len(self.buffer_2) == self.buffer_2.maxlen:
      delayed_frame2 = self.buffer_2.popleft()
      self.__display_frame(self.monitor_2, delayed_frame2, "MISSION CONTROL")

  def __process_live_frames(self, frame1, frame2):
    self.__display_frame(self.monitor_1, frame1, "LUNAR BASE")
    self.__display_frame(self.monitor_2, frame2, "MISSION CONTROL")

  def __display_frame(self, monitor, frame, overlay_text):
    if frame is not None:
      frame = self.__add_overlay(frame, overlay_text)
      monitor.show_frame(frame)
    else:
      print(f"No frame captured for {overlay_text}.")

  def __add_overlay(self, frame, top_left_text):
    # Define colors
    blue_color = (255, 0, 0)  # Blue in BGR
    white_color = (255, 255, 255)  # White in BGR

    # Define font and scale
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.3  # Small font scale for bottom-right text
    thickness = 2  # Slightly increased thickness for better readability

    # Add top-left text with blue box
    top_left_text_size = cv2.getTextSize(top_left_text, font, 1, 2)[0]
    top_left_box_coords = (0, 0, top_left_text_size[0] + 10, top_left_text_size[1] + 10)
    cv2.rectangle(frame, (top_left_box_coords[0], top_left_box_coords[1]),
                  (top_left_box_coords[2], top_left_box_coords[3]), blue_color, -1)
    cv2.putText(frame, top_left_text, (top_left_box_coords[0] + 5, top_left_box_coords[3] - 5),
                font, 1, white_color, 2, cv2.LINE_AA)

    # Add bottom-right text with blue box
    bottom_right_text_line1 = "*A sound delay has been added to represent the time it takes"
    bottom_right_text_line2 = "for sound to travel from Earth to the Moon. (1.5 seconds)"
    bottom_right_text_size_line1 = cv2.getTextSize(bottom_right_text_line1, font, font_scale, thickness)[0]
    bottom_right_text_size_line2 = cv2.getTextSize(bottom_right_text_line2, font, font_scale, thickness)[0]
    frame_height, frame_width = frame.shape[:2]

    # Calculate the box size to fit both lines
    box_width = max(bottom_right_text_size_line1[0], bottom_right_text_size_line2[0]) + 10
    box_height = bottom_right_text_size_line1[1] + bottom_right_text_size_line2[1] + 15
    bottom_right_box_coords = (frame_width - box_width - 10,
                               frame_height - box_height - 10,
                               frame_width - 10,
                               frame_height - 10)

    # Draw the blue box
    cv2.rectangle(frame, (bottom_right_box_coords[0], bottom_right_box_coords[1]),
                  (bottom_right_box_coords[2], bottom_right_box_coords[3]), blue_color, -1)

    # Add the first line of text
    cv2.putText(frame, bottom_right_text_line1,
                (bottom_right_box_coords[0] + 5, bottom_right_box_coords[1] + bottom_right_text_size_line1[1] + 5),
                font, font_scale, white_color, thickness, cv2.LINE_AA)

    # Add the second line of text
    cv2.putText(frame, bottom_right_text_line2,
                (bottom_right_box_coords[0] + 5, bottom_right_box_coords[1] + bottom_right_text_size_line1[1] + bottom_right_text_size_line2[1] + 10),
                font, font_scale, white_color, thickness, cv2.LINE_AA)

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

