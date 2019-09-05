from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import keras.backend as K
from tensorflow.python.keras.models import load_model
from cf_keras import LRN
import pickle
import tensorflow as tf

import os
from tensorflow.python.keras.callbacks import TensorBoard

path="data\\resized"
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
#sess=K.Session()
model=load_model('fuse/fusew37.h5', custom_objects={"LRN":LRN})

model.summary()
input("any key continue")

train_datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    validation_split=0.2,
    horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(
        'data/resized',  # this is the target directory
        target_size=(image_size, image_size),  # all images will be resized
        batch_size=batch_size,
        subset="training",
        class_mode='categorical')  # categorical label
validation_generator = train_datagen.flow_from_directory(
        'data/resized',  # this is the target directory
        target_size=(image_size, image_size),  # all images will be resized
        batch_size=batch_size,
        subset="validation",
        class_mode='categorical')  # categorical label

# hislist=[]
# his1=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
#                     validation_data=validation_generator, validation_steps=len(validation_generator), epochs=15, verbose=1)
# model.save("fuse/fusew15.h5")
# hislist.append(his1.history)
# with open("fuse/hislist_f.pk","wb")as f:
#     pickle.dump(hislist,f)
# his2=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
#                     validation_data=validation_generator, validation_steps=len(validation_generator), epochs=15, verbose=1)
# model.save("fuse/fusew30.h5")
# hislist.append(his2.history)
# with open("fuse/hislist_f.pk","wb")as f:
#     pickle.dump(hislist,f)
# his3=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
#                     validation_data=validation_generator, validation_steps=len(validation_generator), epochs=7, verbose=1)
# model.save("fuse/fusew37.h5")
# hislist.append(his3.history)
# with open("fuse/hislist_f.pk","wb")as f:
#     pickle.dump(hislist,f)


tf.summary.FileWriter("logs", tf.get_default_graph())

# hislist = []
# tensorboard = TensorBoard(log_dir='logs/')
# his1=model.fit_generator(train_generator, steps_per_epoch=len(train_generator)*stepfactor,
#                     validation_data=validation_generator, validation_steps=len(validation_generator), epochs=1, verbose=2,callbacks=[tensorboard])