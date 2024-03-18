from flask import Flask, render_template, Response, request
from picamera2 import Picamera2
import io
import time
from PIL import Image

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
        # Convert the NumPy array to a JPEG image in memory
        img_io = io.BytesIO()
        pil_image = Image.fromarray(frame.astype('uint8'), 'RGB')  # Create a PIL Image from the NumPy array
        pil_image.save(img_io, 'JPEG')  # Save the PIL image as JPEG to the BytesIO buffer
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
