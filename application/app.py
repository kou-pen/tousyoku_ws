from flask import Flask, render_template, Response,request
from camera import Camera,Camera2
import cv2
import numpy as np
from PIL import Image
import io
from face_detect import face_detect_truth


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data/')
def data():
    return render_template('data.html')

@app.route('/face/', methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        name = request.form['facename']
        cap(Camera(),name)
        return render_template('face.html')
    elif request.method == 'GET':
        return render_template('face.html')
            
@app.route('/stream1/')
def stream1():
    return render_template('camera1.html')        

@app.route('/stream2/')
def stream2():
    return render_template('camera2.html')

def gen(camera,st):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame+ b"\r\n")
        else:
            print('frame is none')
        
def cap(camera,name):
    frame = camera.get_frame()
    if frame is not None:
        new_name = './pic/'+name+'.jpg'
        num_byteio = io.BytesIO(frame)
        with Image.open(num_byteio) as img:
            num_numpy = np.asarray(img)
        new_image = np.array(num_numpy)
        flag = face_detect_truth(new_image)
        if not flag:
            cv2.imwrite(new_name,new_image,[cv2.IMWRITE_JPEG_QUALITY, 100])
            print("saved")
        else:
            print("Already known")
    else:
        print('frame is none')

@app.route("/cam1/")
def video_feed1():
    return Response(gen(Camera(),1),
            mimetype="multipart/x-mixed-replace; boundary=frame")
    
@app.route("/cam2/")
def video_feed2():
    return Response(gen(Camera2(),2),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/cam3/")
def video_feed3():
    return Response(gen(Camera(),3),
            mimetype="multipart/x-mixed-replace; boundary=frame")

    
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')