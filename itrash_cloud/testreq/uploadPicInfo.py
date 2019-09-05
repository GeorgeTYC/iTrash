import requests
import os

BASE_DIR=os.path.dirname(os.path.abspath(__file__))
ur='http://127.0.0.1:8000/upload'

files={'img':('apple12.jpg',open(os.path.join(BASE_DIR,'apple.jpg'),'rb'),'image/jpg',{})}

#f = open(r'F:\5k_test_set\5k_test_set\expertC_gt\a4502-Duggan_090116_4368.jpg','rb')
res=requests.request("POST",url=ur,data={"pred":"fruit","mid":3},files=files)
print(res.content)
#r = requests.request("POST",ur,files={'files':f})
#users_dic = r.json()
#print(users_dic)
