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

class videoController:
    def __init__(self, webcam_1, webcam_2, monitor_1, monitor_2):
        self.webcam_1_index = webcam_1
        self.webcam_2_index = webcam_2
        self.monitor_1_index = monitor_1
        self.monitor_2_index = monitor_2
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

        if frame2 is not None:
            self.monitor_2.show_frame(frame2)

    def run(self):
        try:
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
    monitor_test = videoController(0, 2, 0, 1)
    if monitor_test.init():
        videoThread = threading.Thread(target=monitor_test.run)
        videoThread.start()

        try:
            while True:
                time.sleep(1)
                print("Monitor test Running...")
        except KeyboardInterrupt:
            with monitor_test.LOCK:
                monitor_test.EXIT = True
            videoThread.join()
        print("Monitor test finished.")
    else:
        print("Failed to initialize videoController.")