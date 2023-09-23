# system module
import io
import configparser
import os

# Image Processing module
import cv2
import numpy as np
from PIL import Image

# Flask module
from flask import Flask, render_template, Response, request, send_file, url_for, redirect, flash
from flask import session as sess

# User module
from modules.camera import *
from modules.face_detect import face_detect_truth
from modules.sql_tool import *
from modules.aruco_generator  import *
from modules.api_led import ApiLed
import modules.pdftools as pd

# camera define
def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame+ b"\r\n")
        else:
            print('frame is none')
        
def cap(camera,name,save):
    frame = camera.get_frame()
    if frame is not None:
        new_name = 'pic/'+name+'.jpeg'
        num_byteio = io.BytesIO(frame)
        with Image.open(num_byteio) as img:
            num_numpy = np.asarray(img)
        new_image = np.array(num_numpy)
        detect_flag ,names= face_detect_truth(new_image)
        
        if not save:
            return detect_flag ,names
        
        if not detect_flag:
            if os.path.isfile(new_name):
                flash("すでに同様のファイル名が存在します")
                return
            new_image = cv2.cvtColor(new_image,cv2.COLOR_RGB2BGR)
            cv2.imwrite(new_name,new_image,[cv2.IMWRITE_JPEG_QUALITY, 100])
            ins_data = User(user_name = name,file_name = new_name)
            db_tool.insert(ins_data)
            flash(name + "として保存されました")
        else:
            flash(names + "としてすでに登録済みです")
      
    else:
        print('frame is none')
        

# Aruco Define 
# TODO:Do Classify
def check_aruco(camera):
    dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dict_aruco,parameters)
    count = 0
    while True:
        api.toggle_led()
        frame = camera.get_frame()
        if frame is not None:
            num_byteio = io.BytesIO(frame)
            with Image.open(num_byteio) as img:
                num_numpy = np.asarray(img)
            new_image = np.array(num_numpy)
            gray = cv2.cvtColor(new_image,cv2.COLOR_RGB2GRAY)
            corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
            frame_markers = aruco.drawDetectedMarkers(new_image.copy(), corners, ids)
            frame_markers = cv2.cvtColor(frame_markers,cv2.COLOR_RGB2BGR)
            frame_markers = cv2.imencode('.jpg', frame_markers)[1].tobytes()
            
            aruco_list = np.ravel(ids).tolist()
            truth_result = compare_aruco_db(UsingMarker,aruco_list)
            if len(truth_result) == 0:
                count = 0
            else:
                count += 1
            
            if count > 50:
                not_found_handler(truth_result)
                count = 0
                break
            
            yield (b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_markers+ b"\r\n")
        else:
            print('frame is none')
            
def compare_aruco_db(table,aruco_list):
    datas = db_tool.search_user(table,0)
    if datas == None:
        return True
    if aruco_list == None:
        return False
    
    result = []
    for data in datas:
        if data.mark not in aruco_list :
            result.append(data.mark)
    return result

def not_found_handler(result):
    text = ' '.join(map(str,result))
    
    text = text + ' が見つかりません!'
    api.line_notify(text)
    
    
# Configparser
config = configparser.ConfigParser()
config.read('config.ini')
default = config['DEFAULT']

GET_URL = 'http://192.168.0.10:8000/status'
POST_URL = 'http://192.168.0.10:8000/toggle'
LINE_TOKEN = 'Yi1UAVve4DbuaADyUld2W1cGuwMEBqLRqoRoDjD075q'
th = 1000
        
# Make Flask Ob
app = Flask(__name__)
app.secret_key = default['Secret_key']

# Make instance
db_tool = DataBaseTools(Base)
api = ApiLed(th,GET_URL,POST_URL,LINE_TOKEN)

#Routing
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
            flash("有効な選択肢を選んでください")
            return render_template("foodin.html")
        datas = db_tool.search_aruco(UsingMarker,int(aruco_id))
        datas.user_name = name
        db_tool.update()
        flash("登録されました")
        return redirect(url_for("foodlist"))

@app.route('/food/out/auth', methods=['GET', 'POST'])
def food_out_auth():
    if request.method == 'GET':
        datas = db_tool.get_all(User)
        return render_template("foodoutauth.html",datas=datas)
    elif request.method == 'POST':
        username = request.form['username']
        if username == "0":
            flash("有効な選択肢を選んでください")
            return redirect(url_for("food_out_auth"))
        detect_flag ,names = cap(Camera(),username,0)
        if detect_flag==False or names!=username:
            flash("認証に失敗")
            return render_template("foodoutauth.html")
        sess["name"] = username
        flash("認証に成功")
        return redirect(url_for("food_out"))
    
@app.route("/food/out",methods=['GET', 'POST'])
def food_out():
    if request.method == 'GET':
        username = sess["name"]
        datas = db_tool.search_name(UsingMarker,username)
        return render_template("foodoutmenu.html",datas=datas)
    elif request.method == 'POST':
        aruco_id = request.form["mark"]
        if aruco_id == "0":
            flash("有効な選択肢を選んでください")
            return redirect(url_for("food_out"))
        data = db_tool.search_aruco(UsingMarker,aruco_id)
        db_tool.delete(data)
        flash("取り出しました")
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
    return Response(check_aruco(Camera2()),
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

        flash("作成されました")
        return send_file(pdf_path,as_attachment=True)


# Main
if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=5000)