from flask import Flask, render_template, Response, request
from picamera import PiCamera
from io import BytesIO
import time

app = Flask(__name__)
camera = PiCamera()
camera.resolution = (640, 480)  # Set your desired resolution

def gen(camera):
    """Video streaming generator function."""
    stream = BytesIO()
    for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        stream.seek(0)
        frame = stream.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        stream.seek(0)
        stream.truncate()

@app.route('/video_feed')
def video_feed():
    """Route to stream video."""
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/take_picture')
def take_picture():
    """Route to take a picture."""
    camera.capture('/home/pi/Desktop/image.jpg')  # Adjust the path as needed
    return ('', 204)

@app.route('/')
def index():
    """The index page with streaming video and a button to take a picture."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
