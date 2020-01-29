#coding: utf-8

import argparse
import glob
import cv2
import matplotlib.pyplot as plt
import os

#----------------------------------------
# 引数の処理

parser = argparse.ArgumentParser(description="Convert from Face Image to Mosaic Image")
parser.add_argument("-i", "--input", help="Input Directory", required=True)
parser.add_argument("-o", "--output", help="Output Directory", required=True)
parser.add_argument("--show", help="Show Images", action="store_true")
parser.add_argument("--scale", help="Scale Factor", type=float, default=1.1)
parser.add_argument("--neighbor", help="Min Neighbors", type=int, default=5)
args = parser.parse_args()

INPUT_DIR = args.input
OUTPUT_DIR = args.output
SHOW_FLG = args.show
SCALE = args.scale
NEIGHBOR = args.neighbor
#----------------------------------------

#----------------------------------------
# 画像ファイルの取得

images = []
gray_images = []

paths = sorted(glob.glob(INPUT_DIR + "/*.jpg"))

for path in paths:
    print(path)
    image = cv2.imread(path)
    images.append(image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_images.append(gray_image)
#----------------------------------------


#----------------------------------------
# 正面顔検出
def detect_face(image):
    
    haar_cascade_face = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
    faces = haar_cascade_face.detectMultiScale(image, scaleFactor=SCALE, minNeighbors=NEIGHBOR)
    print("Frontal-Faces:" + str(len(faces)))
    
    return faces
#----------------------------------------

#----------------------------------------
# 横顔検出

def detect_pface(image):

    haar_cascade_pface = cv2.CascadeClassifier("cascades/haarcascade_profileface.xml")
    pfaces = haar_cascade_pface.detectMultiScale(image, scaleFactor=SCALE, minNeighbors=NEIGHBOR)
    print("Profile-Faces:" + str(len(pfaces)))
    
    return pfaces
#----------------------------------------

#----------------------------------------
# 体検出

def detect_body(image):

    haar_cascade_body = cv2.CascadeClassifier("cascades/haarcascade_fullbody.xml")
    bodies = haar_cascade_body.detectMultiScale(image, scaleFactor=SCALE, minNeighbors=NEIGHBOR)
    print("Bodies:" + str(len(bodies)))
    
    return bodies
#----------------------------------------

#----------------------------------------
# モザイク処理

def makeMosaic(image, x, y, w, h):
    cut_img = image[y:y+h, x:x+w]
    cut_face = cut_img.shape[:2][::-1]
    cut_img = cv2.resize(cut_img, (cut_face[0]//10, cut_face[0]//10))
    cut_img = cv2.resize(cut_img, cut_face, interpolation = cv2.INTER_NEAREST)
    image[y:y+h,x:x+w] = cut_img
#----------------------------------------

#----------------------------------------
# 画像の保存

def save(path, image):
    save_path = OUTPUT_DIR + "/" + "mosaic_" + os.path.basename(path)
    cv2.imwrite(save_path, image)
    print(save_path)
#----------------------------------------


#----------------------------------------    
# モザイク処理と保存

results = zip(paths, images)

for (path, image) in results:

    faces = detect_face(image)
    pfaces = detect_pface(image)
    bodies = detect_body(image)    
    
    for(x, y, w, h) in faces:
        makeMosaic(image, x, y, w, h)    

    for(x, y, w, h) in pfaces:
        makeMosaic(image, x, y, w, h)        

    for(x, y, w, h) in bodies:
        makeMosaic(image, x, y, w, h)                

    save(path, image)
        
    if SHOW_FLG:
        plt.imshow(image)
        plt.show()
#----------------------------------------
