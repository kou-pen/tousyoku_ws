import cv2
import numpy as np
import face_recognition
import os

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
        if face_recognition.face_encodings(img) == None:
            encode = None
        else:
            try:
                if face_recognition.face_encodings(img)[0].size != 0:
                    encode = face_recognition.face_encodings(img)[0]
                else:
                    encode = None
            except IndexError:
                encode = None
            
        encode_list.append(encode)
        print(len(encode_list))
        print(encode_list)
    return encode_list

def face_detect_truth(img):
    images,classNames = search_path()
    encode_list_known = master_encodings(images)

    img_resize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2RGB)

    matches = []
    person = 0
    try:
        encode_frame = face_recognition.face_encodings(img_resize)[0]
        matches = face_recognition.compare_faces(encode_list_known, encode_frame)
        face_distances = face_recognition.face_distance(encode_list_known, encode_frame)
        best_match_index = np.argmin(face_distances)
        if face_distances.size != 0:
            person = classNames[best_match_index]
        else:
            person = None
    except IndexError:
        matches.append(False)
    
    return True in matches, person
