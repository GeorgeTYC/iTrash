from tensorflow.python.keras.models import load_model
from tensorflow.python import keras
import tensorflow as tf
import numpy as np
import cv2
import os

keras.backend.clear_session()
graph = tf.get_default_graph()
MODEL_DIR=os.path.join(os.path.dirname(os.path.abspath(__file__)),"resnet50w15_0.h5")
model = load_model(MODEL_DIR)
print('load model...')
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
print('load done.')
print('test model...')
with graph.as_default():
    print(model.predict(np.zeros((1, 224,224,3))))
print('test done.')

labellist=["apple","banana","baozhuangdai","battery","dry wet trash","empty","fruits","medicine","paper","plastic bottle"]


def interpret(word_label):
    c=0
    max=0
    label1 = None
    label2 = None
    for i,v in enumerate(word_label):
        if max<v:
            max=v
            c=i
    label1=labellist[c]
    return label1


def classify_ResNet(img_path):
    IMG_SIZE = 224
    img = cv2.imread(img_path)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    arr = np.array(img)
    with graph.as_default():
        pre = model.predict(arr.reshape(-1, IMG_SIZE, IMG_SIZE, 3))
    print("pre:", pre)
    lbl = interpret(pre[0])
    print("lbl:", lbl)
    return lbl

if __name__=="__main__":
    img_path="D:\\xiaoxueqi\\itrash_cloud\\media\\tmp\\bottle.jpg"
    classify_ResNet(img_path)
