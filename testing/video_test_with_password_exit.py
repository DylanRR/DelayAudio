import cv2
import time
from screeninfo import get_monitors
import tkinter as tk
from tkinter import simpledialog

# Define the correct password
CORRECT_PASSWORD = "pass"

def ask_password():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    password = simpledialog.askstring("Password", "Enter the password:", show='*')
    root.destroy()
    return password

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
    monitor_a = monitors[0]  # Primary monitor
    monitor_b = monitors[1]  # Secondary monitor

    # Monitor A properties
    screen_width_a = monitor_a.width
    screen_height_a = monitor_a.height
    screen_x_a = monitor_a.x
    screen_y_a = monitor_a.y

    # Monitor B properties
    screen_width_b = monitor_b.width
    screen_height_b = monitor_b.height
    screen_x_b = monitor_b.x
    screen_y_b = monitor_b.y

    # Create named windows
    cv2.namedWindow('Webcam 1', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Webcam 2', cv2.WINDOW_NORMAL)

    # Move windows to respective monitors
    cv2.moveWindow('Webcam 1', screen_x_a, screen_y_a)
    cv2.moveWindow('Webcam 2', screen_x_b, screen_y_b)

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
        frame1 = cv2.resize(frame1, (screen_width_a, screen_height_a))
        frame2 = cv2.resize(frame2, (screen_width_b, screen_height_b))

        # Display frames
        cv2.imshow('Webcam 1', frame1)
        cv2.imshow('Webcam 2', frame2)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            password = ask_password()
            if password == CORRECT_PASSWORD:
                break
            else:
                print("Incorrect password. Program will continue running.")

    # Release the captures and close the windows
    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()