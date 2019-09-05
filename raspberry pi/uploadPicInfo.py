import requests
import os
import time

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
ur='http://192.168.137.66:8000/upload'

def upload(trashtype):
    print("uplaoding start")
    files={'img':(str(int(time.time()))+'_1.jpg',open(os.path.join(BASE_DIR,'cut.jpg'),'rb'),'image/jpg',{})}
    res=requests.request("POST",url=ur,data={"pred":trashtype,"mid":1},files=files,headers={'Connection':'close'})
    print("upload info:",res.content)
