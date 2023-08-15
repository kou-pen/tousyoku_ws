from flask import Flask, render_template, Response
from camera import Camera

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data/')
def data():
    return render_template('data.html')

@app.route('/face/')
def face():
    return render_template('face.html')
            
@app.route('/stream1/')
def stream1():
    return render_template('camera1.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n")
        else:
            print("frame is none")

@app.route('/stream2/')
def stream2():
    return render_template('camera2.html')

@app.route("/cam1/")
def video_feed1():
    return Response(gen(Camera(0)),
            mimetype="multipart/x-mixed-replace; boundary=frame")
    
@app.route("/cam2/")
def video_feed2():
    return Response(gen(Camera(1)),
            mimetype="multipart/x-mixed-replace; boundary=frame")
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')