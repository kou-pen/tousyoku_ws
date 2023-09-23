import cv2
import glob
import numpy  as np
from PIL import Image
import shutil,os
import datetime
import img2pdf

png_path = './marker/'
pdf_path = './pdf/'

def convert_to_pdf():
    png_file_path = glob.glob(png_path + '*.png')
    len_png_file = len(png_file_path)
    
    height = 0
    width  = 0

    match len_png_file:
        case 24:
            height = 6
            width =  4
        case 40:
            height = 8
            width =  5
        case 54:
            height = 9
            width =  6
        case _:
            return
        
    k = 0
    for i in range(width):
        for j in range(height):
            if k  >= len_png_file:break
            im = np.array(Image.open(png_file_path[k]))
            if j == 0:im1 = im
            else:im1 = np.hstack((im1,im))
            k += 1
        if i == 0:im2 = im1
        else:im2 = np.vstack((im2,im1))
        if k >= len_png_file:break
        
    file_time_name = datetime_ob()
    file_name_out = pdf_path + file_time_name
    cv2.imwrite(file_name_out +".png",im2)
    pdf_out_path = convert_pdf(file_name_out)
    delete_all_png()

    return pdf_out_path
    
    
def convert_pdf(name):
    image_path = name + ".png"
    out_pdf_path = name + ".pdf"
    
    image = Image.open(image_path)
    
    pdf_bytes = img2pdf.convert(image.filename)
    files = open(out_pdf_path,"wb")
    files.write(pdf_bytes)
    
    image.close()
    files.close()
    
    return out_pdf_path
    
def concat_tile(im_list_2d):
    return cv2.vconcat([cv2.hconcat(im_list_h) for im_list_h in im_list_2d])

def delete_all_png():
    shutil.rmtree(png_path)
    os.mkdir(png_path)

def datetime_ob ():
    dt_now = datetime.datetime.now()
    month = dt_now.month
    day = dt_now.day
    hour = dt_now.hour
    mins = dt_now.minute
    sec = dt_now.second
    text = "{}_{}_{}_{}_{}".format(month,day,hour,mins,sec)
    return text
    
if __name__ == '__main__':
    convert_to_pdf()
    