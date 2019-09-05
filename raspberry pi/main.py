#coding:utf-8
from barcodecat import bclassify
import os
from audiocat import cat_audiohint,audioinput
import trashbox
import time
import warnings
from neuralcat import nclassify
from uploadPicInfo import upload
import threading
from picamera import PiCamera, Color

warnings.filterwarnings('ignore')
#camera=PiCamera()
#camera.saturation=80
#camera.brightness=50
#camera.shutter_speed=6000000
#camera.iso=800

while True:
    os.system("raspistill -o shot.jpg -q 100 -br 60 --ISO 300")
    #camera.capture("shot.jpg")
    #camera.close()
    nclass=nclassify("shot.jpg")
    if nclass=="empty":
        print('nothing')
        time.sleep(2)
        continue
    bclass=bclassify("shot.jpg")
    print("barcode:",bclass)
    print("nn:",nclass)
    if bclass:
        trashtype=bclass
    elif nclass:
        trashtype=nclass
    else:
        trashtype=audioinput()
    cat=cat_audiohint(trashtype,1)
    print(cat)
    t1=threading.Thread(target=upload, args=(trashtype,))
    t1.start()
    print(cat)
    if cat:
        trashbox.open(cat)
    


