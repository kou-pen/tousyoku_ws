import io

import cv2
import numpy as np
from PIL import Image

from flask import Flask, render_template, Response, request, send_file, url_for, redirect, flash
from flask import session as sess

from modules.camera import *
from modules.face_detect import face_detect_truth
from modules.sql_tool import *
from modules.aruco_generator  import *
import modules.pdftools as pd

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame+ b"\r\n")
        else:
            flash('frame is none')
        
def cap(camera,name,save):
    frame = camera.get_frame()
    if frame is not None:
        new_name = 'pic/'+name+'.jpg'
        num_byteio = io.BytesIO(frame)
        with Image.open(num_byteio) as img:
            num_numpy = np.asarray(img)
        new_image = np.array(num_numpy)
        detect_flag ,names= face_detect_truth(new_image)
        
        if not save:
            return detect_flag ,names
        
        if not detect_flag:
            if os.path.isfile(new_name):
                flash("file already exists")
                return
            cv2.imwrite(new_name,new_image,[cv2.IMWRITE_JPEG_QUALITY, 100])
            ins_data = User(user_name = name,file_name = new_name)
            db_tool.insert(ins_data)
            flash("saved as "+name)
        else:
            flash("Already known as " + names)
      
    else:
        flash('frame is none')
        

db_tool = DataBaseTools(Base)

app = Flask(__name__)
app.secret_key = 'abcdefghijklmn'


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/data/')
def data():
    datas = db_tool.get_all(User)
    return render_template('data.html',datas=datas)

@app.route('/food/in', methods=['GET', 'POST'])
def food_in():
    if request.method == 'GET':
        userdatas = db_tool.get_all(User)
        labeldatas =  db_tool.search_user(UsingMarker,1)
        return render_template("foodin.html",userdatas=userdatas,labeldatas=labeldatas)
    elif request.method == 'POST':
        name  = request.form['username']
        aruco_id = request.form['number']
        if name == "0" or aruco_id == "0":
            flash("please select aviable dropdown")
            return render_template("foodin.html")
        datas = db_tool.search_aruco(UsingMarker,int(aruco_id))
        datas.user_name = name
        db_tool.update()
        flash("registerd")
        return redirect(url_for("foodlist"))

@app.route('/food/out/auth', methods=['GET', 'POST'])
def food_out_auth():
    if request.method == 'GET':
        datas = db_tool.get_all(User)
        return render_template("foodoutauth.html",datas=datas)
    elif request.method == 'POST':
        username = request.form['username']
        detect_flag ,names = cap(Camera(),username,0)
        if detect_flag==False or names!=username:
            flash("auth faild")
            return render_template("foodoutauth.html")
        sess["name"] = username
        flash("auth successed")
        return redirect(url_for("food_out"))
    
@app.route("/food/out",methods=['GET', 'POST'])
def food_out():
    if request.method == 'GET':
        username = sess["name"]
        datas = db_tool.search_name(UsingMarker,username)
        return render_template("foodoutmenu.html",datas=datas)
    elif request.method == 'POST':
        aruco_id = request.form["mark"]
        data = db_tool.search_aruco(UsingMarker,aruco_id)
        db_tool.delete(data)
        flash("retrieved")
        return redirect(url_for("foodlist"))
    
@app.route('/face/', methods=['GET', 'POST'])
def face():
    if request.method == 'POST':
        name = request.form['facename']
        if name == "":
            return render_template("face.html")
        cap(Camera(),name,1)
        return redirect(url_for("data"))
    elif request.method == 'GET':
        return render_template('face.html')
    
@app.route("/foodlist/", methods=['GET'])
def foodlist():
    if request.method == "GET":
        datas = db_tool.search_user(UsingMarker,0)
        return render_template("foodlist.html",datas = datas)
            
@app.route('/stream1/')
def stream1():
    return render_template('camera1.html')        

@app.route('/stream2/')
def stream2():
    return render_template('camera2.html')

@app.route("/cam1/")
def video_feed1():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")
    
@app.route("/cam2/")
def video_feed2():
    return Response(gen(Camera2()),
            mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/cam3/")
def video_feed3():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")
    
@app.route("/cam4/")
def video_feed4():
    return Response(gen(Camera()),
            mimetype="multipart/x-mixed-replace; boundary=frame")
    
@app.route("/else/")
def else_():
    return render_template("else.html")

@app.route("/makemarker/", methods=['GET', 'POST'])
def make_marker():
    if request.method == 'GET':
        return render_template('make_marker.html')
    
    elif request.method == 'POST':
        number = int(request.form['number'])
        
        if number == 0:
            return render_template('make_marker.html')
        marker_data = db_tool.get_limit(NotUsedMarker,number)

        if len(marker_data) == 0:
            db_tool.make_some_marker(1,100)
            marker_data = db_tool.get_limit(NotUsedMarker,number)
        
        all_data = db_tool.get_all(NotUsedMarker)
        query_last = db_tool.get_last(NotUsedMarker)
        
        if len(all_data) <= number:
            db_tool.make_some_marker(query_last.mark + 1,100)
            marker_data = db_tool.get_limit(NotUsedMarker,number)
            
        for data in marker_data:
            filename = "marker/{}.png".format(data.mark)
            ar_gen = ArucoGenerator()
            ar_gen.generate_marker(filename,data.mark)
            using_marker_data  = UsingMarker(mark=data.mark,user_name="")
            db_tool.insert(using_marker_data)
            db_tool.delete(data)
            
        pdf_path = pd.convert_to_pdf()
        # pd.delete_all_png()
        flash("created")
        return send_file(pdf_path,as_attachment=True)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=5000)