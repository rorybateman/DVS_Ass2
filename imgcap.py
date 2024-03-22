# imgcap.py
'''
Main file to run the image capture and live recognition
'''
import os
import time
import cv2
from Live_recognition import live
# Open the default camera (0 for the first camera)
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Unable to open the camera")
    exit()

# Capture a frame from the camera
ret, frame = cap.read()

# Check if the frame was captured successfully
if not ret:
    print("Error: Failed to capture a frame from the camera")
    cap.release()
    exit()


# Run another Python file
while True:
    try:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture a frame from the camera")
            break
        # Display the captured frame
        cv2.imshow("Captured Frame", frame)

        # Save the captured frame as an image file
        cv2.imwrite(f"captured_image.jpg", frame)

        # Wait for 1 seconds
        cv2.waitKey(1000)
        live('captured_image.jpg')
    except KeyboardInterrupt:
        print("interputed")
        time.sleep(0.5)
        cap.release()
        cv2.destroyAllWindows()
    