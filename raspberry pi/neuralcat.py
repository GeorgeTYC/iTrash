from keras.models import load_model
from PIL import Image
import numpy as np

IMG_SIZE=224

print("Initializing Model...")
model=load_model("resnet50w15_10.h5")
model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])
print("Initialize OK")


def interpret(word_label):
    labellist = ['apple','banana','baozhuangdai','battery','dry wet trash','empty','fruits','medicine','paper','pen','plastic bottle']
    c=0
    max=0
    label1 = None
    for i,v in enumerate(word_label):
        if max<v:
            max=v
            c=i
    if max>0.5:
        label1=labellist[c]
    return label1


def nclassify(path):
    global IMG_SIZE
    img=Image.open(path,"r")
    box = (375, 125, 1875, 1625)
    #box = (250, 0, 2000, 1750)
    img = img.crop(box)
    img.save('cut.jpg')
    img=img.resize((IMG_SIZE,IMG_SIZE))
    arr=np.array(img)
    pre=model.predict(arr.reshape(-1,IMG_SIZE,IMG_SIZE,3))
    print(pre[0])
    return interpret(pre[0])