# camera.py

import cv2
from cv2 import aruco

class Camera(object):
    dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)
    parameters = aruco.DetectorParameters()
    def __init__(self):
        self.video = cv2.VideoCapture(4)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        corners, ids, rejectedImgPoints = aruco.detect(gray, self.dict_aruco, parameters=self.parameters)
        
        frame_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)
        
        ret, frame = cv2.imencode('.jpg', frame_markers)
        return frame
