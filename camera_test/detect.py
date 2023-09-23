import cv2
from cv2 import aruco
import numpy as np
import time

dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)
parameters = aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(dict_aruco, parameters)

cap = cv2.VideoCapture(2) #usb 4 pc 0

try:
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = detector.detectMarkers(gray)

        frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
        cv2.imshow('frame', frame_markers)
        print(np.ravel(ids).tolist())
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow('frame')
    cap.release()
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()