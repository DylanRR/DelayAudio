import cv2

def list_webcams():
    webcams = []
    for i in range (10):  # Scan through device numbers 0-9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            webcams.append(i)
            cap.release()
    return webcams

def identify_webcams():
    webcams = list_webcams()
    caps = [cv2.VideoCapture(i) for i in webcams]

    while True:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if ret:
                # Overlay the device number on the webcam feed
                cv2.putText(frame, f"Device {webcams[i]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Add note to use esc to exit
                cv2.putText(frame, "Press ESC to exit", (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1)
                cv2.imshow(f"Webcam {webcams[i]}", frame)

            # Check if the window is closed
            if cv2.getWindowProperty(f"Webcam {webcams[i]}", cv2.WND_PROP_VISIBLE) < 1:
                break

        # Check if any window is closed
        if any(cv2.getWindowProperty(f"Webcam {webcams[i]}", cv2.WND_PROP_VISIBLE) < 1 for i in range(len(webcams))):
            break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    for cap in caps:
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Detected webcams at:", list_webcams())
    identify_webcams()