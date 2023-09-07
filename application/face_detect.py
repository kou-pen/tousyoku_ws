import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

def search_path():
    path = 'pic'
    images = []
    classNames = []
    myList = os.listdir(path)
    
    for cls in myList:
        current_img = cv2.imread(f'{path}/{cls}')
        images.append(current_img)
        classNames.append(os.path.splitext(cls)[0])
    return images,classNames

def master_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

def face_detect_truth(img):
    images,classNames = search_path()
    encode_list_known = master_encodings(images)

    img_resize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

    matches = []
    try:
        encode_frame = face_recognition.face_encodings(img_resize)[0]
        matches = face_recognition.compare_faces(encode_list_known, encode_frame)
    except IndexError:
        matches.append(False)
    
    return True in matches
