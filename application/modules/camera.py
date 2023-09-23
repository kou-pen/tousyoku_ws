import cv2
from modules.base_camera import BaseCamera
from modules.base_camera2 import BaseCamera2


class Camera(BaseCamera):
    def __init__(self):
        super().__init__()

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(2)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
            
class Camera2(BaseCamera2):
    def __init__(self):
        super().__init__()

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
