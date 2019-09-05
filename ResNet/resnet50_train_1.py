from keras import backend as K
from tensorflow.python.keras.models import Model
import numpy as np
from keras.applications.resnet50 import ResNet50
from keras.layers import Input, GlobalAveragePooling2D, Dense, Dropout, Activation, Flatten
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import pickle
import os
# from tensorflow.python.keras.callbacks import TensorBoard

path="data\\Training"
dir_count=0
for filename in os.listdir(path):
    newpath = os.path.join(path, filename)
    if os.path.isdir(newpath):
        dir_count += 1
print(dir_count)
image_size=224
num_classes=dir_count
batch_size=11
stepfactor=1.4

K.set_learning_phase(0)
Inp = Input((image_size, image_size,3))
base_model = ResNet50(weights='imagenet', include_top=False,
                      input_shape=(image_size, image_size,3))

K.set_learning_phase(1)
x = base_model(Inp)
x = GlobalAveragePooling2D(name='average_pool')(x)
#x=Dense(200, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)
for layer in base_model.layers[0:-30]:
    layer.trainable = False
model = Model(inputs=Inp, outputs=predictions)
model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=["accuracy"])

model.summary()
input("any key continue")

train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    validation_split=0.2,
    horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
        'data/Training',  # this is the target directory
        target_size=(image_size, image_size),  # all images will be resized
        batch_size=batch_size,
        subset="training",
        class_mode='categorical')  # categorical label
validation_generator = train_datagen.flow_from_directory(
        'data/Training',  # this is the target directory
        target_size=(image_size, image_size),  # all images will be resized
        batch_size=batch_size,
        subset="validation",
        class_mode='categorical')  # categorical label

hislist=[]
his1=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
                    validation_data=validation_generator, validation_steps=len(validation_generator), epochs=15, verbose=1)
model.save("resnet101/resnet101w15_0.h5")
hislist.append(his1.history)
with open("resnet101/hislist0.pk","wb")as f:
    pickle.dump(hislist,f)
his2=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
                    validation_data=validation_generator, validation_steps=len(validation_generator), epochs=15, verbose=1)
model.save("resnet101/resnet101w30_0.h5")
hislist.append(his2.history)
with open("resnet101/hislist0.pk","wb")as f:
    pickle.dump(hislist,f)
his3=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
                    validation_data=validation_generator, validation_steps=len(validation_generator), epochs=7, verbose=1)
model.save("resnet101/resnet101w37_0.h5")
hislist.append(his3.history)
with open("resnet101/hislist0.pk","wb")as f:
    pickle.dump(hislist,f)

# hislist = []
# tensorboard = TensorBoard(log_dir='logs/')
# his1=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
#                     validation_data=validation_generator, validation_steps=len(validation_generator), epochs=1, verbose=2,callbacks=[tensorboard])