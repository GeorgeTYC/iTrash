import os
import tensorflow
from tensorflow.python.keras.models import load_model,Model
from tensorflow.python.keras.layers import concatenate,Input,Dense,Flatten
from cf_keras import LRN

Inp = Input(shape=(224, 224, 3))
net=load_model("../20/resnet50w37_0.h5")
caffeModel=load_model('../caffe_keras.h5', custom_objects={"LRN":LRN})
path="../data/resized"

def merge_model():

    model1 = Model(inputs=net.input, outputs=net.layers[-2].output,name="ResNet_model")
    model2 = Model(inputs=caffeModel.input, outputs=caffeModel.layers[-2].output,name="MINC_model")
    r1 = model1(Inp)
    r2 = model2(Inp)  # 获得输出

    flus = concatenate([r1, r2])  # 拼接输出，融合成功

    model = Model(inputs=Inp, outputs=flus)
    return model



def modify():  # 这里修改模型
    origin_model = merge_model()
    for layer in origin_model.layers:
        layer.trainable = False  # 原来的不训练

    inp = origin_model.input
    x = origin_model.output

    fl=Flatten(name='flatten')(x)
    den = Dense(1000, activation='relu',name="dense1")(fl)
    dir_count=0
    for filename in os.listdir(path):
        newpath = os.path.join(path, filename)
        if os.path.isdir(newpath):
            dir_count += 1
    result = Dense(dir_count, activation="softmax",name="output")(den)

    model = Model(inputs=inp, outputs=result)
    model.summary()
    # 编译model
    # adam = keras.optimizers.Adam(lr=0.0005, beta_1=0.95, beta_2=0.999, epsilon=1e-08)
    # adam = keras.optimizers.Adam(lr = 0.001, beta_1=0.95, beta_2=0.999,epsilon=1e-08)
    #sgd = keras.optimizers.SGD(lr = 0.001, decay = 1e-06, momentum = 0.9, nesterov = False)

    # reduce_lr = ReduceLROnPlateau(monitor = 'loss', factor = 0.1, patience = 2,verbose = 1, min_lr = 0.00000001, mode = 'min')
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


newModel=modify()
newModel.save('../fuse/fuse.h5')