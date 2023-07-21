import cv2
from cv2 import aruco
import os

dir_mark = r'/home/kohki/tousyoku_ws/camera_test/pic' #folder

num_mark = 20 #num
size_mark = 500 #size

dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)

for count in range(num_mark) :

    id_mark = count  # id
    img_mark = aruco.generateImageMarker(dict_aruco, id_mark, size_mark)

    if count < 10 :
        img_name_mark = 'mark_id_0' + str(count) + '.jpg'
    else :
        img_name_mark = 'mark_id_' + str(count) + '.jpg'
    path_mark = os.path.join(dir_mark, img_name_mark)

    cv2.imwrite(path_mark, img_mark)