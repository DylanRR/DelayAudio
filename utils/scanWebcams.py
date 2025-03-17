import cv2

def list_webcams():
    webcams = []
    for i in range(10):  # Scan through device numbers 0-9
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            webcams.append(i)
            cap.release()
    return webcams

print("Detected webcams at:", list_webcams())
