import cv2
import time
from screeninfo import get_monitors

def main():
    # Open both webcams
    cap1 = cv2.VideoCapture(0)  # Webcam 1
    cap2 = cv2.VideoCapture(2)  # Webcam 2

    if not cap1.isOpened():
        print("Error: Could not open webcam 1.")
        return
    if not cap2.isOpened():
        print("Error: Could not open webcam 2.")
        return

    # Get screen resolutions of all monitors
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

    while True:
        # Capture frames from both webcams
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

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
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
