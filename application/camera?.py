# camera.py

import cv2

class Camera(object):
    def __init__(self,cam_num):
        self.video = cv2.VideoCapture(cam_num)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if success:
            ret, frame = cv2.imencode('.jpg', image)
            return frame
        else:
            return None