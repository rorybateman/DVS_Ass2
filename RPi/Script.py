from flask import Flask, render_template, Response, request
from picamera2 import Picamera2
import io
import time
from PIL import Image
import cv2

app = Flask(__name__)
picamera2 = Picamera2()
preview_config = picamera2.create_preview_configuration(main={"size": (640, 480)})
picamera2.configure(preview_config)
picamera2.start()

import numpy as np

def generate_frame(picamera2):
    """Video streaming generator function."""
    while True:
        # Capture the image in NumPy format
        frame = picamera2.capture_array()
        # Ensure the frame is in the right format (RGB, uint8)
        if frame.dtype != np.uint8:
            frame = frame.astype(np.uint8)
        # Convert from YUV to RGB if needed (This is just an example. Actual conversion depends on the camera output)
        if picamera2.camera_properties['PixelFormat'] == 'YUV420':
            frame = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB)
        # Convert the NumPy array to a PIL Image
        pil_image = Image.fromarray(frame, 'RGB')  # Create a PIL Image from the NumPy array
        # Convert to JPEG
        img_io = io.BytesIO()
        pil_image.save(img_io, 'JPEG', quality=70)  # Adjust quality as needed
        img_io.seek(0)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_io.getvalue() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Route to stream video."""
    return Response(generate_frame(picamera2),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_picture')
def take_picture():
    """Route to take a picture."""
    picamera2.capture_file('/home/pi/Desktop/image.jpg')
    return ('', 204)

@app.route('/')
def index():
    """The index page with streaming video and a button to take a picture."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
