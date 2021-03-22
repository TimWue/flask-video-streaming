from flask import Flask, render_template, Response
import logging
from camera_opencv import Camera
#import threading


app = Flask(__name__)
'''
def executeStream():
    logging.info("Started Stream")
    while True:
        #sleep(2)
        my_file = open('static/stream.jpg', 'wb')
        with picamera.PiCamera() as camera:
            camera.capture(my_file)
        my_file.close()
'''
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    #x = threading.Thread(target=executeStream, daemon=True)
    #x.start()
    app.run(host='0.0.0.0', debug=True, threaded=True)